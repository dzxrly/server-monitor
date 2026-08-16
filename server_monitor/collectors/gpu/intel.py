from __future__ import annotations

from typing import Any


class IntelGpuProvider:
    """Reserved provider boundary for a future Intel implementation."""

    provider_name = "intel"

    @staticmethod
    def collect() -> dict[str, Any]:
        return {
            "available": False,
            "provider": "intel",
            "devices": [],
            "processes": [],
            "reason": "Intel GPU metrics are not implemented yet.",
        }

    @staticmethod
    def close() -> None:
        return None
