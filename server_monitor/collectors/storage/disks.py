from __future__ import annotations

import time
from typing import Any

import psutil


class DiskCollector:
    """Collect mounted-volume capacity and physical-device I/O rates."""

    def __init__(self) -> None:
        self._last_io: dict[str, Any] = {}
        self._last_sample_time: float | None = None

    @staticmethod
    def _volumes() -> list[dict[str, Any]]:
        volumes: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for partition in psutil.disk_partitions(all=False):
            key = (partition.device.casefold(), partition.mountpoint.casefold())
            if key in seen:
                continue
            seen.add(key)
            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except (FileNotFoundError, OSError, PermissionError):
                continue
            options = [option for option in partition.opts.split(",") if option]
            volumes.append(
                {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fileSystem": partition.fstype or None,
                    "options": options,
                    "readOnly": "ro" in options,
                    "totalBytes": usage.total,
                    "usedBytes": usage.used,
                    "freeBytes": usage.free,
                    "usagePercent": float(usage.percent),
                }
            )
        return sorted(volumes, key=lambda item: (item["mountpoint"], item["device"]))

    def _devices(self, now: float) -> list[dict[str, Any]]:
        try:
            current = psutil.disk_io_counters(perdisk=True, nowrap=True) or {}
        except (NotImplementedError, OSError):
            current = {}
        elapsed = (
            max(now - self._last_sample_time, 1e-6) if self._last_sample_time is not None else None
        )
        devices: list[dict[str, Any]] = []
        for name, counters in current.items():
            previous = self._last_io.get(name)

            def rate(
                field: str,
                counters: Any = counters,
                previous: Any = previous,
                elapsed: float | None = elapsed,
            ) -> float | None:
                if previous is None or elapsed is None:
                    return None
                delta = getattr(counters, field, 0) - getattr(previous, field, 0)
                return max(0.0, float(delta) / elapsed)

            devices.append(
                {
                    "name": name,
                    "readCount": counters.read_count,
                    "writeCount": counters.write_count,
                    "readBytes": counters.read_bytes,
                    "writeBytes": counters.write_bytes,
                    "readBytesPerSecond": rate("read_bytes"),
                    "writeBytesPerSecond": rate("write_bytes"),
                    "readOperationsPerSecond": rate("read_count"),
                    "writeOperationsPerSecond": rate("write_count"),
                    "busyTimeMilliseconds": getattr(counters, "busy_time", None),
                }
            )
        self._last_io = current
        self._last_sample_time = now
        return sorted(devices, key=lambda item: item["name"].casefold())

    def collect(self) -> dict[str, Any]:
        now = time.monotonic()
        volumes = self._volumes()
        devices = self._devices(now)
        return {
            "available": bool(volumes or devices),
            "volumes": volumes,
            "devices": devices,
        }
