"""GPU providers."""

from server_monitor.collectors.gpu.amd import AmdGpuProvider
from server_monitor.collectors.gpu.intel import IntelGpuProvider
from server_monitor.collectors.gpu.nvidia import NvidiaGpuProvider

__all__ = ["AmdGpuProvider", "IntelGpuProvider", "NvidiaGpuProvider"]
