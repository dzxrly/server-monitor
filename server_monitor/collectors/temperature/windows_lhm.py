from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import Any


class LibreHardwareMonitorTemperatureProvider:
    """Read Windows hardware sensors through LibreHardwareMonitorLib.dll."""

    provider_name = "librehardwaremonitor"

    def __init__(self, library_path: Path, enabled: bool = True) -> None:
        self._library_path = library_path
        self._enabled = enabled
        self._computer: Any = None
        self._sensor_type: Any = None
        self._load_error: str | None = None

    def _ensure_open(self) -> None:
        if self._computer is not None or self._load_error is not None:
            return
        if not self._enabled:
            self._load_error = "LibreHardwareMonitor integration is disabled."
            return
        if not self._library_path.is_file():
            self._load_error = f"Library not found: {self._library_path}"
            return
        try:
            import clr

            clr.AddReference(str(self._library_path))
            from LibreHardwareMonitor.Hardware import Computer, SensorType

            computer = Computer()
            for property_name in (
                "IsCpuEnabled",
                "IsGpuEnabled",
                "IsMemoryEnabled",
                "IsMotherboardEnabled",
                "IsControllerEnabled",
                "IsStorageEnabled",
                "IsNetworkEnabled",
            ):
                if hasattr(computer, property_name):
                    setattr(computer, property_name, True)
            computer.Open()
            self._computer = computer
            self._sensor_type = SensorType
        except Exception as error:  # pythonnet/.NET errors vary by runtime
            self._load_error = f"{type(error).__name__}: {error}"

    def _walk_hardware(self, hardware: Any, sensors: list[dict[str, Any]]) -> None:
        hardware.Update()
        hardware_name = str(hardware.Name)
        hardware_type = str(hardware.HardwareType)
        for sensor in hardware.Sensors:
            if sensor.SensorType != self._sensor_type.Temperature or sensor.Value is None:
                continue
            sensors.append(
                {
                    "hardware": hardware_name,
                    "hardwareType": hardware_type,
                    "name": str(sensor.Name),
                    "identifier": str(sensor.Identifier),
                    "currentCelsius": float(sensor.Value),
                    "highCelsius": (
                        float(sensor.Max) if getattr(sensor, "Max", None) is not None else None
                    ),
                    "criticalCelsius": None,
                }
            )
        for sub_hardware in hardware.SubHardware:
            self._walk_hardware(sub_hardware, sensors)

    def collect(self) -> dict[str, Any]:
        self._ensure_open()
        if self._computer is None:
            return {
                "available": False,
                "provider": self.provider_name,
                "sensors": [],
                "cpu": [],
                "reason": self._load_error,
            }
        sensors: list[dict[str, Any]] = []
        try:
            for hardware in self._computer.Hardware:
                self._walk_hardware(hardware, sensors)
        except Exception as error:  # hardware plugins can throw provider-specific errors
            return {
                "available": False,
                "provider": self.provider_name,
                "sensors": [],
                "cpu": [],
                "reason": f"{type(error).__name__}: {error}",
            }
        cpu_sensors = [
            sensor.copy()
            for sensor in sensors
            if "cpu" in sensor.get("hardwareType", "").casefold()
            or "cpu" in sensor["hardware"].casefold()
        ]
        return {
            "available": bool(sensors),
            "provider": self.provider_name,
            "sensors": sensors,
            "cpu": cpu_sensors,
            "reason": None if sensors else "No readable temperature sensors were reported.",
        }

    def close(self) -> None:
        if self._computer is not None:
            with suppress(Exception):
                self._computer.Close()
            self._computer = None
