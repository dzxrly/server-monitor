from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from server_monitor.collectors.network.interfaces import NetworkCollector
from server_monitor.collectors.processes.top import TopProcessCollector
from server_monitor.collectors.storage.disks import DiskCollector
from server_monitor.collectors.system.cpu import _linux_cpu_name
from server_monitor.collectors.temperature.windows_lhm import (
    LibreHardwareMonitorTemperatureProvider,
)


def test_disk_collector_reports_all_volumes_and_rates(monkeypatch) -> None:
    samples = iter(
        [
            {
                "disk0": SimpleNamespace(
                    read_count=1, write_count=2, read_bytes=100, write_bytes=200, busy_time=5
                )
            },
            {
                "disk0": SimpleNamespace(
                    read_count=3, write_count=5, read_bytes=300, write_bytes=500, busy_time=8
                )
            },
        ]
    )
    times = iter([10.0, 12.0])
    monkeypatch.setattr(
        "server_monitor.collectors.storage.disks.psutil.disk_partitions",
        lambda all: [SimpleNamespace(device="C:", mountpoint="C:\\", fstype="NTFS", opts="rw")],
    )
    monkeypatch.setattr(
        "server_monitor.collectors.storage.disks.psutil.disk_usage",
        lambda mountpoint: SimpleNamespace(total=1000, used=400, free=600, percent=40.0),
    )
    monkeypatch.setattr(
        "server_monitor.collectors.storage.disks.psutil.disk_io_counters",
        lambda perdisk, nowrap: next(samples),
    )
    monkeypatch.setattr(
        "server_monitor.collectors.storage.disks.time.monotonic", lambda: next(times)
    )

    collector = DiskCollector()
    first = collector.collect()
    second = collector.collect()

    assert first["volumes"][0]["mountpoint"] == "C:\\"
    assert first["devices"][0]["readBytesPerSecond"] is None
    assert second["devices"][0]["readBytesPerSecond"] == 100.0
    assert second["devices"][0]["writeBytesPerSecond"] == 150.0


def test_network_collector_reports_interfaces_and_rates(monkeypatch) -> None:
    samples = iter(
        [
            {
                "Ethernet": SimpleNamespace(
                    bytes_sent=100,
                    bytes_recv=200,
                    packets_sent=1,
                    packets_recv=2,
                    errin=0,
                    errout=0,
                    dropin=0,
                    dropout=0,
                )
            },
            {
                "Ethernet": SimpleNamespace(
                    bytes_sent=300,
                    bytes_recv=500,
                    packets_sent=3,
                    packets_recv=5,
                    errin=0,
                    errout=0,
                    dropin=0,
                    dropout=0,
                )
            },
        ]
    )
    times = iter([20.0, 22.0])
    monkeypatch.setattr(
        "server_monitor.collectors.network.interfaces.psutil.net_io_counters",
        lambda pernic, nowrap: next(samples),
    )
    monkeypatch.setattr(
        "server_monitor.collectors.network.interfaces.psutil.net_if_stats",
        lambda: {"Ethernet": SimpleNamespace(isup=True, duplex=2, speed=1000, mtu=1500)},
    )
    monkeypatch.setattr(
        "server_monitor.collectors.network.interfaces.psutil.net_if_addrs", lambda: {}
    )
    monkeypatch.setattr(
        "server_monitor.collectors.network.interfaces.time.monotonic", lambda: next(times)
    )

    collector = NetworkCollector()
    first = collector.collect()
    second = collector.collect()

    assert first["interfaces"][0]["bytesSentPerSecond"] is None
    assert second["interfaces"][0]["bytesSentPerSecond"] == 100.0
    assert second["interfaces"][0]["bytesReceivedPerSecond"] == 150.0
    assert second["totals"]["bytesReceived"] == 500


def test_librehardwaremonitor_missing_library_degrades_cleanly(tmp_path: Path) -> None:
    provider = LibreHardwareMonitorTemperatureProvider(tmp_path / "missing.dll")
    result = provider.collect()

    assert result["available"] is False
    assert result["provider"] == "librehardwaremonitor"
    assert "Library not found" in result["reason"]


def test_top_process_collector_excludes_windows_idle_process(monkeypatch) -> None:
    idle = SimpleNamespace(
        info={
            "pid": 0,
            "name": "System Idle Process",
            "create_time": 1.0,
            "cpu_times": SimpleNamespace(user=100.0, system=0.0),
            "memory_info": SimpleNamespace(rss=0),
            "memory_percent": 0.0,
        }
    )
    worker = SimpleNamespace(
        info={
            "pid": 42,
            "name": "worker.exe",
            "create_time": 2.0,
            "cpu_times": SimpleNamespace(user=5.0, system=1.0),
            "memory_info": SimpleNamespace(rss=1024),
            "memory_percent": 1.0,
        }
    )
    inaccessible = SimpleNamespace(
        info={
            "pid": 99,
            "name": None,
            "create_time": None,
            "cpu_times": None,
            "memory_info": None,
            "memory_percent": None,
        }
    )
    monkeypatch.setattr(
        "server_monitor.collectors.processes.top.psutil.process_iter",
        lambda attributes: [idle, inaccessible, worker],
    )

    result = TopProcessCollector().collect(limit=5)

    assert [row["pid"] for row in result["cpu"]] == [42]
    assert [row["pid"] for row in result["memory"]] == [42]


def test_linux_cpu_name_prefers_model_over_processor_index() -> None:
    cpuinfo = """processor : 0
vendor_id : GenuineIntel
model name : Example CPU 9000
processor : 1
model name : Example CPU 9000
"""

    assert _linux_cpu_name(cpuinfo) == "Example CPU 9000"


def test_linux_cpu_name_accepts_descriptive_arm_processor() -> None:
    assert _linux_cpu_name("Processor : ARMv7 Processor rev 3 (v7l)\n") == (
        "ARMv7 Processor rev 3 (v7l)"
    )
