from __future__ import annotations

import time
from collections import defaultdict
from contextlib import suppress
from typing import Any


def _decode(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


class NvidiaGpuProvider:
    """NVML-backed NVIDIA device and process collector."""

    provider_name = "nvidia-nvml"

    def __init__(self) -> None:
        self._nvml: Any = None
        self._initialized = False
        self._load_error: str | None = None
        self._last_process_timestamp: dict[int, int] = {}

    def _ensure_initialized(self) -> None:
        if self._initialized or self._load_error is not None:
            return
        try:
            import pynvml

            pynvml.nvmlInit()
            self._nvml = pynvml
            self._initialized = True
        except Exception as error:
            self._load_error = f"{type(error).__name__}: {error}"

    def _optional(self, function_name: str, *args: Any) -> Any:
        try:
            function = getattr(self._nvml, function_name)
            return function(*args)
        except Exception:
            return None

    def _running_processes(self, handle: Any, device_index: int) -> list[dict[str, Any]]:
        records: dict[int, dict[str, Any]] = {}
        for function_names, process_type in (
            (
                (
                    "nvmlDeviceGetComputeRunningProcesses_v3",
                    "nvmlDeviceGetComputeRunningProcesses",
                ),
                "compute",
            ),
            (
                (
                    "nvmlDeviceGetGraphicsRunningProcesses_v3",
                    "nvmlDeviceGetGraphicsRunningProcesses",
                ),
                "graphics",
            ),
        ):
            processes = None
            for function_name in function_names:
                processes = self._optional(function_name, handle)
                if processes is not None:
                    break
            if processes is None:
                continue
            for process in processes:
                pid = int(process.pid)
                used_memory = getattr(process, "usedGpuMemory", None)
                if used_memory is not None and (used_memory < 0 or used_memory >= (1 << 63)):
                    used_memory = None
                record = records.setdefault(
                    pid,
                    {
                        "pid": pid,
                        "gpuMemoryBytes": 0,
                        "gpuUsagePercent": None,
                        "deviceIndexes": [],
                        "types": [],
                    },
                )
                if used_memory is not None:
                    record["gpuMemoryBytes"] += int(used_memory)
                if device_index not in record["deviceIndexes"]:
                    record["deviceIndexes"].append(device_index)
                if process_type not in record["types"]:
                    record["types"].append(process_type)
        utilization_samples = self._optional(
            "nvmlDeviceGetProcessUtilization",
            handle,
            self._last_process_timestamp.get(device_index, 0),
        )
        latest_timestamp = int(time.time() * 1_000_000)
        for sample in utilization_samples or []:
            pid = int(sample.pid)
            record = records.setdefault(
                pid,
                {
                    "pid": pid,
                    "gpuMemoryBytes": 0,
                    "gpuUsagePercent": None,
                    "deviceIndexes": [],
                    "types": [],
                },
            )
            usage = float(getattr(sample, "smUtil", 0))
            previous_usage = record["gpuUsagePercent"]
            record["gpuUsagePercent"] = (
                usage if previous_usage is None else max(previous_usage, usage)
            )
            if device_index not in record["deviceIndexes"]:
                record["deviceIndexes"].append(device_index)
            latest_timestamp = max(
                latest_timestamp, int(getattr(sample, "timeStamp", latest_timestamp))
            )
        self._last_process_timestamp[device_index] = latest_timestamp
        return list(records.values())

    def collect(self) -> dict[str, Any]:
        self._ensure_initialized()
        if not self._initialized:
            return {
                "available": False,
                "provider": self.provider_name,
                "devices": [],
                "processes": [],
                "reason": self._load_error,
            }
        try:
            count = int(self._nvml.nvmlDeviceGetCount())
        except Exception as error:
            return {
                "available": False,
                "provider": self.provider_name,
                "devices": [],
                "processes": [],
                "reason": f"{type(error).__name__}: {error}",
            }

        devices: list[dict[str, Any]] = []
        process_records: dict[int, dict[str, Any]] = defaultdict(
            lambda: {
                "pid": 0,
                "gpuMemoryBytes": 0,
                "gpuUsagePercent": None,
                "deviceIndexes": [],
                "types": [],
            }
        )
        for index in range(count):
            try:
                handle = self._nvml.nvmlDeviceGetHandleByIndex(index)
                name = _decode(self._nvml.nvmlDeviceGetName(handle))
                memory = self._optional("nvmlDeviceGetMemoryInfo", handle)
                utilization = self._optional("nvmlDeviceGetUtilizationRates", handle)
                temperature = self._optional(
                    "nvmlDeviceGetTemperature", handle, self._nvml.NVML_TEMPERATURE_GPU
                )
                power_milliwatts = self._optional("nvmlDeviceGetPowerUsage", handle)
                power_limit_milliwatts = self._optional("nvmlDeviceGetEnforcedPowerLimit", handle)
                devices.append(
                    {
                        "index": index,
                        "name": name,
                        "uuid": _decode(self._optional("nvmlDeviceGetUUID", handle) or ""),
                        "driverVersion": _decode(
                            self._optional("nvmlSystemGetDriverVersion") or ""
                        ),
                        "usagePercent": (
                            float(utilization.gpu) if utilization is not None else None
                        ),
                        "memoryUsagePercent": (
                            float(utilization.memory) if utilization is not None else None
                        ),
                        "memory": {
                            "totalBytes": int(memory.total) if memory is not None else None,
                            "usedBytes": int(memory.used) if memory is not None else None,
                            "freeBytes": int(memory.free) if memory is not None else None,
                        },
                        "temperatureCelsius": (
                            float(temperature) if temperature is not None else None
                        ),
                        "fanSpeedPercent": self._optional("nvmlDeviceGetFanSpeed", handle),
                        "powerWatts": (
                            float(power_milliwatts) / 1000 if power_milliwatts is not None else None
                        ),
                        "powerLimitWatts": (
                            float(power_limit_milliwatts) / 1000
                            if power_limit_milliwatts is not None
                            else None
                        ),
                    }
                )
                for process in self._running_processes(handle, index):
                    pid = process["pid"]
                    merged = process_records[pid]
                    merged["pid"] = pid
                    merged["gpuMemoryBytes"] += process["gpuMemoryBytes"]
                    usage = process["gpuUsagePercent"]
                    if usage is not None:
                        previous_usage = merged["gpuUsagePercent"]
                        merged["gpuUsagePercent"] = (
                            usage if previous_usage is None else max(previous_usage, usage)
                        )
                    for device_index in process["deviceIndexes"]:
                        if device_index not in merged["deviceIndexes"]:
                            merged["deviceIndexes"].append(device_index)
                    for process_type in process["types"]:
                        if process_type not in merged["types"]:
                            merged["types"].append(process_type)
            except Exception:
                continue
        return {
            "available": bool(devices),
            "provider": self.provider_name,
            "devices": devices,
            "processes": list(process_records.values()),
            "reason": None if devices else "No readable NVIDIA GPU was found.",
        }

    def close(self) -> None:
        if self._initialized:
            with suppress(Exception):
                self._nvml.nvmlShutdown()
        self._initialized = False
