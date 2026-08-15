from __future__ import annotations

import platform
from pathlib import Path
from typing import Any

import psutil

from server_monitor.collectors.common import safe_call


def _linux_cpu_name(cpuinfo: str) -> str | None:
    candidates: dict[str, str] = {}
    for line in cpuinfo.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized_key = key.strip().casefold()
        normalized_value = value.strip()
        if not normalized_value:
            continue
        if normalized_key in {"model name", "hardware"} or (
            normalized_key == "processor" and not normalized_value.isdecimal()
        ):
            candidates.setdefault(normalized_key, normalized_value)
    for key in ("model name", "hardware", "processor"):
        if key in candidates:
            return candidates[key]
    return None


def _cpu_name() -> str:
    if psutil.WINDOWS:
        try:
            import winreg

            path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                return str(winreg.QueryValueEx(key, "ProcessorNameString")[0]).strip()
        except (ImportError, OSError):
            pass
    if psutil.LINUX:
        try:
            name = _linux_cpu_name(
                Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="ignore")
            )
            if name:
                return name
        except OSError:
            pass
    return platform.processor().strip() or platform.machine() or "Unknown"


class CpuCollector:
    def __init__(self) -> None:
        self.name = _cpu_name()
        psutil.cpu_percent(interval=None, percpu=True)
        psutil.cpu_percent(interval=None, percpu=False)

    @staticmethod
    def _frequency() -> dict[str, float | None]:
        frequency = safe_call(lambda: psutil.cpu_freq(percpu=False), None)
        if frequency is None:
            return {"currentMhz": None, "minMhz": None, "maxMhz": None}
        return {
            "currentMhz": float(frequency.current) if frequency.current else None,
            "minMhz": float(frequency.min) if frequency.min else None,
            "maxMhz": float(frequency.max) if frequency.max else None,
        }

    def collect(self) -> dict[str, Any]:
        per_cpu = psutil.cpu_percent(interval=None, percpu=True)
        average = psutil.cpu_percent(interval=None, percpu=False)
        stats = safe_call(psutil.cpu_stats, None)
        result: dict[str, Any] = {
            "available": True,
            "name": self.name,
            "usagePercent": float(average),
            "perCoreUsagePercent": [float(value) for value in per_cpu],
            "physicalCores": psutil.cpu_count(logical=False),
            "logicalCores": psutil.cpu_count(logical=True),
            "frequency": self._frequency(),
            "temperatures": [],
        }
        if stats is not None:
            result["statistics"] = {
                "contextSwitches": stats.ctx_switches,
                "interrupts": stats.interrupts,
                "softInterrupts": stats.soft_interrupts,
                "syscalls": stats.syscalls,
            }
        return result
