from __future__ import annotations

import os
import platform
import socket
import time
from typing import Any

import psutil


class OperatingSystemCollector:
    @staticmethod
    def collect() -> dict[str, Any]:
        uname = platform.uname()
        os_name = uname.system
        os_version = uname.release
        if psutil.WINDOWS:
            edition = platform.win32_edition()
            os_name = f"Windows {edition}".strip()
            os_version = platform.version()
        elif psutil.LINUX:
            try:
                release = platform.freedesktop_os_release()
                os_name = release.get("PRETTY_NAME") or release.get("NAME") or os_name
                os_version = release.get("VERSION_ID") or os_version
            except (AttributeError, OSError):
                pass
        boot_time = psutil.boot_time()
        return {
            "available": True,
            "name": os_name,
            "version": os_version,
            "kernel": uname.release,
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "bits": platform.architecture()[0],
            "hostname": socket.gethostname(),
            "bootTimeEpochSeconds": boot_time,
            "uptimeSeconds": max(0.0, time.time() - boot_time),
            "processId": os.getpid(),
            "pythonVersion": platform.python_version(),
        }
