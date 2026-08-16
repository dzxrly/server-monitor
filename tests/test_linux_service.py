from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_linux_service_renderer_keeps_working_directory_absolute(tmp_path: Path) -> None:
    project_root = Path(__file__).parents[1]
    output_path = tmp_path / "server-monitor.service"
    renderer = project_root / "deploy" / "linux" / "render_service.py"

    subprocess.run(
        [sys.executable, str(renderer), str(project_root), str(output_path)],
        check=True,
    )

    service = output_path.read_text(encoding="utf-8")
    expected_root = str(project_root.resolve())
    assert f"WorkingDirectory={expected_root}" in service
    assert f'WorkingDirectory="{expected_root}"' not in service
    assert 'ExecStart="' in service
