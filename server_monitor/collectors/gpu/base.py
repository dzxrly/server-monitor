from __future__ import annotations

from typing import Any, Protocol


class GpuProvider(Protocol):
    provider_name: str

    def collect(self) -> dict[str, Any]: ...

    def close(self) -> None: ...
