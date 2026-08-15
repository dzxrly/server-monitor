from __future__ import annotations

import time
from typing import Any

import psutil


class TopProcessCollector:
    """Rank CPU, memory and GPU processes without blocking the sampler."""

    def __init__(self) -> None:
        self._last_cpu_times: dict[tuple[int, float], float] = {}
        self._last_sample_time: float | None = None
        self._logical_cpu_count = max(1, psutil.cpu_count(logical=True) or 1)

    def collect(
        self, limit: int, gpu_processes: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        now = time.monotonic()
        elapsed = (
            max(now - self._last_sample_time, 1e-6) if self._last_sample_time is not None else None
        )
        current_cpu_times: dict[tuple[int, float], float] = {}
        rows: list[dict[str, Any]] = []
        process_names: dict[int, str] = {}

        for process in psutil.process_iter(
            ["pid", "name", "create_time", "cpu_times", "memory_info", "memory_percent"]
        ):
            try:
                info = process.info
                create_time = float(info["create_time"] or 0.0)
                key = (int(info["pid"]), create_time)
                cpu_times = info["cpu_times"]
                total_cpu_time = float(cpu_times.user + cpu_times.system)
                current_cpu_times[key] = total_cpu_time
                previous_cpu_time = self._last_cpu_times.get(key)
                cpu_percent = 0.0
                if previous_cpu_time is not None and elapsed is not None:
                    cpu_percent = max(
                        0.0,
                        min(
                            100.0,
                            (total_cpu_time - previous_cpu_time)
                            / elapsed
                            / self._logical_cpu_count
                            * 100.0,
                        ),
                    )
                name = info["name"] or f"PID {info['pid']}"
                process_names[int(info["pid"])] = name
                # Windows exposes the scheduler's idle counter as PID 0. It is
                # not a user process and would otherwise dominate the CPU list.
                if int(info["pid"]) == 0:
                    continue
                rows.append(
                    {
                        "pid": int(info["pid"]),
                        "name": name,
                        "cpuUsagePercent": cpu_percent,
                        "memoryUsagePercent": float(info["memory_percent"] or 0.0),
                        "memoryBytes": int(info["memory_info"].rss),
                    }
                )
            except (
                AttributeError,
                KeyError,
                TypeError,
                ValueError,
                psutil.AccessDenied,
                psutil.NoSuchProcess,
                psutil.ZombieProcess,
            ):
                continue

        self._last_cpu_times = current_cpu_times
        self._last_sample_time = now
        cpu = sorted(
            rows, key=lambda row: (row["cpuUsagePercent"], row["memoryBytes"]), reverse=True
        )[:limit]
        memory = sorted(
            rows, key=lambda row: (row["memoryBytes"], row["cpuUsagePercent"]), reverse=True
        )[:limit]

        gpu: list[dict[str, Any]] = []
        for record in gpu_processes or []:
            pid = int(record["pid"])
            name = process_names.get(pid)
            if name is None:
                try:
                    name = psutil.Process(pid).name()
                except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                    name = f"PID {pid}"
            gpu.append(
                {
                    "pid": pid,
                    "name": name,
                    "gpuUsagePercent": record.get("gpuUsagePercent"),
                    "gpuMemoryBytes": record.get("gpuMemoryBytes", 0),
                    "deviceIndexes": record.get("deviceIndexes", []),
                    "types": record.get("types", []),
                }
            )
        gpu.sort(
            key=lambda row: (
                row["gpuUsagePercent"] if row["gpuUsagePercent"] is not None else -1,
                row["gpuMemoryBytes"],
            ),
            reverse=True,
        )
        return {"available": True, "cpu": cpu, "memory": memory, "gpu": gpu[:limit]}
