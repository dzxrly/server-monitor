from __future__ import annotations

from typing import Any

import psutil

_CPU_SENSOR_GROUPS = {
    "coretemp",
    "k10temp",
    "zenpower",
    "cpu_thermal",
    "soc_thermal",
    "acpitz",
}


class LinuxTemperatureProvider:
    provider_name = "psutil"

    @staticmethod
    def collect() -> dict[str, Any]:
        try:
            groups = psutil.sensors_temperatures(fahrenheit=False)
        except (AttributeError, NotImplementedError, OSError):
            groups = {}
        sensors: list[dict[str, Any]] = []
        cpu_sensors: list[dict[str, Any]] = []
        for group_name, entries in groups.items():
            for index, entry in enumerate(entries):
                sensor = {
                    "hardware": group_name,
                    "name": entry.label or f"Sensor {index + 1}",
                    "currentCelsius": float(entry.current),
                    "highCelsius": float(entry.high) if entry.high is not None else None,
                    "criticalCelsius": (
                        float(entry.critical) if entry.critical is not None else None
                    ),
                }
                sensors.append(sensor)
                lowered = group_name.casefold()
                if lowered in _CPU_SENSOR_GROUPS or any(
                    token in lowered for token in ("cpu", "coretemp", "k10temp")
                ):
                    cpu_sensors.append(sensor.copy())
        return {
            "available": bool(sensors),
            "provider": "psutil",
            "sensors": sensors,
            "cpu": cpu_sensors,
            "reason": None if sensors else "No readable temperature sensors were reported.",
        }

    @staticmethod
    def close() -> None:
        return None
