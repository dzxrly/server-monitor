from __future__ import annotations

from typing import Any


class AmdGpuProvider:
    """Reserved provider boundary for a future AMD implementation."""

    provider_name = "amd"

    @staticmethod
    def collect() -> dict[str, Any]:
        return {
            "available": False,
            "provider": "amd",
            "devices": [],
            "processes": [],
            "reason": "AMD GPU metrics are not implemented yet.",
        }

    @staticmethod
    def close() -> None:
        return None
