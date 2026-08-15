from __future__ import annotations

import atexit
import logging
from typing import Any

from flask import Flask, jsonify
from flask_cors import CORS

from server_monitor.api import create_v1_blueprint
from server_monitor.config import Settings
from server_monitor.services import MetricsSampler


def create_app(
    settings: Settings | None = None,
    *,
    start_sampler: bool = True,
) -> Flask:
    resolved_settings = settings or Settings.from_env()
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    CORS(
        app,
        resources={r"/api/v1/*": {"origins": list(resolved_settings.cors_origins)}},
    )

    sampler = MetricsSampler(resolved_settings)
    app.extensions["metrics_sampler"] = sampler
    app.register_blueprint(create_v1_blueprint(sampler, resolved_settings))

    @app.errorhandler(404)
    def not_found(_: Any) -> tuple[Any, int]:
        return jsonify({"error": "Not found.", "apiVersion": "v1"}), 404

    @app.errorhandler(500)
    def internal_error(error: Any) -> tuple[Any, int]:
        logging.getLogger(__name__).exception("Unhandled request error", exc_info=error)
        return jsonify({"error": "Internal server error.", "apiVersion": "v1"}), 500

    if start_sampler:
        sampler.start()
        atexit.register(sampler.close)
    return app
