from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        return default
    return min(maximum, max(minimum, value))


def _env_float(name: str, default: float, minimum: float, maximum: float) -> float:
    try:
        value = float(os.getenv(name, str(default)))
    except ValueError:
        return default
    return min(maximum, max(minimum, value))


@dataclass(frozen=True)
class Settings:
    host: str = "0.0.0.0"
    port: int = 6543
    sample_interval_seconds: float = 2.0
    max_process_limit: int = 50
    default_process_limit: int = 5
    cors_origins: tuple[str, ...] = ("*",)
    enable_librehardwaremonitor: bool = True
    librehardwaremonitor_path: Path = (
        PROJECT_ROOT / "vendor" / "librehardwaremonitor" / "LibreHardwareMonitorLib.dll"
    )
    log_directory: Path = PROJECT_ROOT / "log"

    @classmethod
    def from_env(cls) -> Settings:
        origins = tuple(
            origin.strip()
            for origin in os.getenv("SERVER_MONITOR_CORS_ORIGINS", "*").split(",")
            if origin.strip()
        ) or ("*",)
        lhm_path = Path(
            os.getenv(
                "SERVER_MONITOR_LHM_PATH",
                str(
                    PROJECT_ROOT / "vendor" / "librehardwaremonitor" / "LibreHardwareMonitorLib.dll"
                ),
            )
        ).expanduser()
        max_process_limit = _env_int("SERVER_MONITOR_MAX_PROCESS_LIMIT", 50, 1, 200)
        default_process_limit = _env_int("SERVER_MONITOR_PROCESS_LIMIT", 5, 1, max_process_limit)
        return cls(
            host=os.getenv("SERVER_MONITOR_HOST", "0.0.0.0"),
            port=_env_int("SERVER_MONITOR_PORT", 6543, 1, 65535),
            sample_interval_seconds=_env_float("SERVER_MONITOR_SAMPLE_INTERVAL", 2.0, 0.25, 60.0),
            max_process_limit=max_process_limit,
            default_process_limit=default_process_limit,
            cors_origins=origins,
            enable_librehardwaremonitor=_env_bool("SERVER_MONITOR_ENABLE_LHM", True),
            librehardwaremonitor_path=lhm_path,
            log_directory=Path(
                os.getenv("SERVER_MONITOR_LOG_DIR", str(PROJECT_ROOT / "log"))
            ).expanduser(),
        )
