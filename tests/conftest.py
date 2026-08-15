from __future__ import annotations

from collections.abc import Iterator

import pytest
from flask import Flask

from server_monitor.application import create_app
from server_monitor.config import Settings


@pytest.fixture
def app(tmp_path) -> Iterator[Flask]:
    settings = Settings(
        sample_interval_seconds=0.25,
        max_process_limit=10,
        default_process_limit=3,
        enable_librehardwaremonitor=True,
        librehardwaremonitor_path=tmp_path / "missing-lhm.dll",
        log_directory=tmp_path / "log",
    )
    application = create_app(settings)
    application.config.update(TESTING=True)
    yield application
    application.extensions["metrics_sampler"].close()
