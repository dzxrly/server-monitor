from __future__ import annotations

from typing import Any

import psutil


class MemoryCollector:
    def __init__(self) -> None:
        self._windows_lists = None
        if psutil.WINDOWS:
            # ctypes.wintypes is Windows-only on older Pythons, so import lazily.
            from server_monitor.collectors.system.windows_memory import WindowsMemoryLists

            self._windows_lists = WindowsMemoryLists()

    def collect(self) -> dict[str, Any]:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "available": True,
            "totalBytes": memory.total,
            "availableBytes": memory.available,
            "usedBytes": memory.used,
            "freeBytes": memory.free,
            "sharedBytes": getattr(memory, "shared", None) if psutil.LINUX else None,
            "usagePercent": float(memory.percent),
            "composition": self._composition(memory),
            "swap": {
                "totalBytes": swap.total,
                "usedBytes": swap.used,
                "freeBytes": swap.free,
                "usagePercent": float(swap.percent),
            },
        }

    def _composition(self, memory: Any) -> list[dict[str, Any]] | None:
        """Split physical memory into segments that add up to the total.

        Linux follows the `free` columns; Windows follows Task Manager's memory
        composition bar. Other platforms return None and the UI falls back to
        used/free.
        """
        total = memory.total
        if psutil.LINUX:
            buffers = memory.buffers
            cached = memory.cached
            free = memory.free
            return [
                {"key": "used", "bytes": max(0, total - free - buffers - cached)},
                {"key": "buffers", "bytes": buffers},
                {"key": "cache", "bytes": cached},
                {"key": "free", "bytes": free},
            ]
        if self._windows_lists is not None:
            lists = self._windows_lists.sample()
            if lists is None:
                return None
            modified = lists["modified"]
            standby = lists["standby"]
            free = min(lists["free"], total)
            return [
                {"key": "inUse", "bytes": max(0, total - modified - standby - free)},
                {"key": "modified", "bytes": modified},
                {"key": "standby", "bytes": standby},
                {"key": "free", "bytes": free},
            ]
        return None
