from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from server_monitor.config import Settings
from server_monitor.services.sampler import MetricsSampler


def create_v1_blueprint(sampler: MetricsSampler, settings: Settings) -> Blueprint:
    blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")

    @blueprint.get("/health")
    def health() -> tuple[Any, int]:
        running = sampler.running
        return (
            jsonify(
                {
                    "status": "ok" if running else "degraded",
                    "apiVersion": "v1",
                    "samplerRunning": running,
                }
            ),
            200 if running else 503,
        )

    @blueprint.get("/capabilities")
    def capabilities() -> Any:
        return jsonify({"apiVersion": "v1", **sampler.capabilities()})

    @blueprint.get("/metrics")
    def metrics() -> tuple[Any, int] | Any:
        raw_limit = request.args.get("processLimit")
        if raw_limit is None:
            process_limit = settings.default_process_limit
        else:
            try:
                process_limit = int(raw_limit)
            except ValueError:
                return jsonify({"error": "processLimit must be an integer."}), 400
            if not 1 <= process_limit <= settings.max_process_limit:
                return (
                    jsonify(
                        {
                            "error": (
                                f"processLimit must be between 1 and {settings.max_process_limit}."
                            )
                        }
                    ),
                    400,
                )
        return jsonify(sampler.snapshot(process_limit))

    return blueprint
