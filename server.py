from __future__ import annotations

import logging

from waitress import serve

from server_monitor.application import create_app
from server_monitor.config import Settings


def main() -> None:
    settings = Settings.from_env()
    settings.log_directory.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(settings.log_directory / "server-monitor.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    app = create_app(settings)
    serve(app, host=settings.host, port=settings.port, threads=8)


if __name__ == "__main__":
    main()
