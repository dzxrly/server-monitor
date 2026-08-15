"""Platform temperature providers."""

from server_monitor.collectors.temperature.base import TemperatureProvider
from server_monitor.collectors.temperature.linux import LinuxTemperatureProvider
from server_monitor.collectors.temperature.windows_lhm import (
    LibreHardwareMonitorTemperatureProvider,
)

__all__ = [
    "TemperatureProvider",
    "LinuxTemperatureProvider",
    "LibreHardwareMonitorTemperatureProvider",
]
