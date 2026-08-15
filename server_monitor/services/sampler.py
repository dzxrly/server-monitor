from __future__ import annotations

import copy
import logging
import platform
import threading
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from server_monitor.collectors.gpu import NvidiaGpuProvider
from server_monitor.collectors.network import NetworkCollector
from server_monitor.collectors.processes import TopProcessCollector
from server_monitor.collectors.storage import DiskCollector
from server_monitor.collectors.system.cpu import CpuCollector
from server_monitor.collectors.system.memory import MemoryCollector
from server_monitor.collectors.system.operating_system import OperatingSystemCollector
from server_monitor.collectors.temperature import (
    LibreHardwareMonitorTemperatureProvider,
    LinuxTemperatureProvider,
)
from server_monitor.config import Settings

LOGGER = logging.getLogger(__name__)


class MetricsSampler:
    """Collect a coherent metrics snapshot on one background cadence."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._cpu = CpuCollector()
        self._memory = MemoryCollector()
        self._operating_system = OperatingSystemCollector()
        self._storage = DiskCollector()
        self._network = NetworkCollector()
        self._nvidia = NvidiaGpuProvider()
        self._processes = TopProcessCollector()
        if platform.system() == "Windows":
            self._temperature = LibreHardwareMonitorTemperatureProvider(
                settings.librehardwaremonitor_path,
                enabled=settings.enable_librehardwaremonitor,
            )
        else:
            self._temperature = LinuxTemperatureProvider()

        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._sequence = 0
        self._snapshot: dict[str, Any] = {
            "apiVersion": "v1",
            "sequence": 0,
            "sampledAt": None,
            "collectionDurationMilliseconds": None,
            "errors": {"sampler": "Metrics have not been sampled yet."},
        }

    @staticmethod
    def _collect(
        name: str,
        function: Callable[[], dict[str, Any]],
        errors: dict[str, str],
    ) -> dict[str, Any]:
        try:
            return function()
        except Exception as error:
            message = f"{type(error).__name__}: {error}"
            errors[name] = message
            LOGGER.exception("Metric collector %s failed", name)
            return {"available": False, "reason": message}

    def _sample_once(self) -> None:
        started = time.monotonic()
        errors: dict[str, str] = {}
        operating_system = self._collect("system", self._operating_system.collect, errors)
        temperatures = self._collect("temperatures", self._temperature.collect, errors)
        cpu = self._collect("cpu", self._cpu.collect, errors)
        cpu["temperatures"] = temperatures.get("cpu", [])
        memory = self._collect("memory", self._memory.collect, errors)
        storage = self._collect("storage", self._storage.collect, errors)
        network = self._collect("network", self._network.collect, errors)
        nvidia = self._collect("gpu.nvidia", self._nvidia.collect, errors)
        processes = self._collect(
            "processes",
            lambda: self._processes.collect(
                self.settings.max_process_limit, nvidia.get("processes", [])
            ),
            errors,
        )
        gpu = {key: value for key, value in nvidia.items() if key != "processes"}

        capabilities = {
            "platform": platform.system().lower(),
            "temperatures": {
                "available": bool(temperatures.get("available")),
                "provider": temperatures.get("provider"),
                "reason": temperatures.get("reason"),
            },
            "gpu": {
                "nvidia": {
                    "available": bool(gpu.get("available")),
                    "provider": gpu.get("provider"),
                    "reason": gpu.get("reason"),
                },
                "amd": {"available": False, "implemented": False},
                "intel": {"available": False, "implemented": False},
            },
            "storage": {"available": bool(storage.get("available"))},
            "network": {"available": bool(network.get("available"))},
            "processes": {"available": bool(processes.get("available"))},
        }
        duration_ms = (time.monotonic() - started) * 1000.0
        with self._lock:
            self._sequence += 1
            self._snapshot = {
                "apiVersion": "v1",
                "sequence": self._sequence,
                "sampledAt": datetime.now(timezone.utc).isoformat(),
                "sampleIntervalSeconds": self.settings.sample_interval_seconds,
                "collectionDurationMilliseconds": duration_ms,
                "system": operating_system,
                "cpu": cpu,
                "memory": memory,
                "gpu": gpu,
                "temperatures": temperatures,
                "storage": storage,
                "network": network,
                "processes": processes,
                "capabilities": capabilities,
                "errors": errors,
            }

    def _run(self) -> None:
        while not self._stop_event.wait(self.settings.sample_interval_seconds):
            cycle_started = time.monotonic()
            self._sample_once()
            collection_time = time.monotonic() - cycle_started
            if collection_time > self.settings.sample_interval_seconds:
                LOGGER.warning(
                    "Metric collection took %.3fs, longer than the %.3fs interval",
                    collection_time,
                    self.settings.sample_interval_seconds,
                )

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._sample_once()
        self._thread = threading.Thread(
            target=self._run,
            name="server-monitor-sampler",
            daemon=True,
        )
        self._thread.start()

    def snapshot(self, process_limit: int) -> dict[str, Any]:
        with self._lock:
            result = copy.deepcopy(self._snapshot)
        processes = result.get("processes", {})
        for key in ("cpu", "memory", "gpu"):
            processes[key] = processes.get(key, [])[:process_limit]
        processes["limit"] = process_limit
        return result

    def capabilities(self) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._snapshot.get("capabilities", {}))

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def close(self) -> None:
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=max(2.0, self.settings.sample_interval_seconds * 2))
        self._nvidia.close()
        self._temperature.close()
