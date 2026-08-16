from __future__ import annotations

import sys
from pathlib import Path


def quote(value: Path | str) -> str:
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: render_service.py PROJECT_ROOT OUTPUT_PATH")
    project_root = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).expanduser()
    template_path = Path(__file__).with_name("server-monitor.service.in")
    log_directory = Path.home() / ".local" / "state" / "server-monitor"
    values = {
        # WorkingDirectory= is parsed as a path rather than as an ExecStart=
        # command line. systemd 249 treats surrounding quotes as literal path
        # characters, so keep this resolved absolute path unquoted.
        "@WORKING_DIRECTORY@": str(project_root),
        "@PYTHON@": quote(project_root / "venv" / "bin" / "python"),
        "@SERVER@": quote(project_root / "server.py"),
        "@LOG_ENVIRONMENT@": quote(f"SERVER_MONITOR_LOG_DIR={log_directory}"),
    }
    service = template_path.read_text(encoding="utf-8")
    for placeholder, value in values.items():
        service = service.replace(placeholder, value)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(service, encoding="utf-8")


if __name__ == "__main__":
    main()
