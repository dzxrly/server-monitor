from __future__ import annotations

import socket
import time
from typing import Any

import psutil


class NetworkCollector:
    """Collect every visible interface and calculate non-blocking transfer rates."""

    def __init__(self) -> None:
        self._last_counters: dict[str, Any] = {}
        self._last_sample_time: float | None = None

    @staticmethod
    def _family_name(family: Any) -> str:
        if family == socket.AF_INET:
            return "ipv4"
        if family == socket.AF_INET6:
            return "ipv6"
        if family == getattr(psutil, "AF_LINK", object()):
            return "mac"
        return str(family)

    def collect(self) -> dict[str, Any]:
        now = time.monotonic()
        try:
            counters = psutil.net_io_counters(pernic=True, nowrap=True) or {}
        except (NotImplementedError, OSError):
            counters = {}
        stats = psutil.net_if_stats()
        addresses = psutil.net_if_addrs()
        elapsed = (
            max(now - self._last_sample_time, 1e-6) if self._last_sample_time is not None else None
        )
        interfaces: list[dict[str, Any]] = []
        total_sent = 0
        total_received = 0
        total_sent_rate = 0.0
        total_received_rate = 0.0
        rates_available = elapsed is not None

        for name in sorted(set(counters) | set(stats) | set(addresses), key=str.casefold):
            current = counters.get(name)
            previous = self._last_counters.get(name)
            interface_stats = stats.get(name)

            def value(field: str, current: Any = current) -> int:
                return int(getattr(current, field, 0)) if current is not None else 0

            def rate(
                field: str,
                current: Any = current,
                previous: Any = previous,
                elapsed: float | None = elapsed,
            ) -> float | None:
                if current is None or previous is None or elapsed is None:
                    return None
                delta = getattr(current, field, 0) - getattr(previous, field, 0)
                return max(0.0, float(delta) / elapsed)

            sent_rate = rate("bytes_sent")
            received_rate = rate("bytes_recv")
            total_sent += value("bytes_sent")
            total_received += value("bytes_recv")
            if sent_rate is not None:
                total_sent_rate += sent_rate
            if received_rate is not None:
                total_received_rate += received_rate

            interface_addresses = [
                {
                    "family": self._family_name(address.family),
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast,
                    "peer": address.ptp,
                }
                for address in addresses.get(name, [])
            ]
            interfaces.append(
                {
                    "name": name,
                    "isUp": bool(interface_stats.isup) if interface_stats else False,
                    "duplex": int(interface_stats.duplex) if interface_stats else None,
                    "speedMbps": interface_stats.speed if interface_stats else None,
                    "mtu": interface_stats.mtu if interface_stats else None,
                    "addresses": interface_addresses,
                    "bytesSent": value("bytes_sent"),
                    "bytesReceived": value("bytes_recv"),
                    "packetsSent": value("packets_sent"),
                    "packetsReceived": value("packets_recv"),
                    "errorsIn": value("errin"),
                    "errorsOut": value("errout"),
                    "dropsIn": value("dropin"),
                    "dropsOut": value("dropout"),
                    "bytesSentPerSecond": sent_rate,
                    "bytesReceivedPerSecond": received_rate,
                }
            )

        self._last_counters = counters
        self._last_sample_time = now
        return {
            "available": bool(interfaces),
            "totals": {
                "bytesSent": total_sent,
                "bytesReceived": total_received,
                "bytesSentPerSecond": total_sent_rate if rates_available else None,
                "bytesReceivedPerSecond": total_received_rate if rates_available else None,
            },
            "interfaces": interfaces,
        }
