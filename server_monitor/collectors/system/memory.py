from __future__ import annotations

from typing import Any

import psutil


class MemoryCollector:
    @staticmethod
    def collect() -> dict[str, Any]:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "available": True,
            "totalBytes": memory.total,
            "availableBytes": memory.available,
            "usedBytes": memory.used,
            "freeBytes": memory.free,
            "usagePercent": float(memory.percent),
            "swap": {
                "totalBytes": swap.total,
                "usedBytes": swap.used,
                "freeBytes": swap.free,
                "usagePercent": float(swap.percent),
            },
        }
