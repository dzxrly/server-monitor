"""Windows memory page lists (Modified / Standby / Free) via PDH counters.

psutil only exposes total/available on Windows. Task Manager's composition bar
comes from the memory manager's page lists, which PDH publishes as gauges.
English counter names are used so localized Windows installs still resolve them.
"""

from __future__ import annotations

import ctypes
import logging
from ctypes import wintypes

LOGGER = logging.getLogger(__name__)

_PDH_FMT_LARGE = 0x00000400
_COUNTERS = {
    "modified": [r"\Memory\Modified Page List Bytes"],
    "standby": [
        r"\Memory\Standby Cache Core Bytes",
        r"\Memory\Standby Cache Normal Priority Bytes",
        r"\Memory\Standby Cache Reserve Bytes",
    ],
    "free": [r"\Memory\Free & Zero Page List Bytes"],
}


class _CounterValueUnion(ctypes.Union):
    _fields_ = [
        ("longValue", wintypes.LONG),
        ("doubleValue", ctypes.c_double),
        ("largeValue", ctypes.c_longlong),
        ("stringValue", wintypes.LPCWSTR),
    ]


class _CounterValue(ctypes.Structure):
    _fields_ = [("CStatus", wintypes.DWORD), ("value", _CounterValueUnion)]


class WindowsMemoryLists:
    def __init__(self) -> None:
        self._pdh = None
        self._query = None
        self._counters: dict[str, list[ctypes.c_void_p]] = {}
        self._disabled = False

    def sample(self) -> dict[str, int] | None:
        if self._disabled:
            return None
        try:
            if self._query is None:
                self._open()
            if self._pdh.PdhCollectQueryData(self._query) != 0:
                return None
            return {
                name: sum(self._read(counter) for counter in counters)
                for name, counters in self._counters.items()
            }
        except Exception as error:  # degrade to used/free in the UI
            LOGGER.warning("Windows memory page lists unavailable: %s", error)
            self._close()
            self._disabled = True
            return None

    def _open(self) -> None:
        pdh = ctypes.WinDLL("pdh")
        pdh.PdhOpenQueryW.argtypes = [
            wintypes.LPCWSTR,
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_void_p),
        ]
        pdh.PdhAddEnglishCounterW.argtypes = [
            ctypes.c_void_p,
            wintypes.LPCWSTR,
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_void_p),
        ]
        pdh.PdhCollectQueryData.argtypes = [ctypes.c_void_p]
        pdh.PdhGetFormattedCounterValue.argtypes = [
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(_CounterValue),
        ]
        pdh.PdhCloseQuery.argtypes = [ctypes.c_void_p]
        for function in (
            pdh.PdhOpenQueryW,
            pdh.PdhAddEnglishCounterW,
            pdh.PdhCollectQueryData,
            pdh.PdhGetFormattedCounterValue,
            pdh.PdhCloseQuery,
        ):
            function.restype = wintypes.DWORD
        self._pdh = pdh

        query = ctypes.c_void_p()
        _check(pdh.PdhOpenQueryW(None, 0, ctypes.byref(query)), "PdhOpenQueryW")
        self._query = query
        for name, paths in _COUNTERS.items():
            handles = []
            for path in paths:
                counter = ctypes.c_void_p()
                _check(
                    pdh.PdhAddEnglishCounterW(query, path, 0, ctypes.byref(counter)),
                    path,
                )
                handles.append(counter)
            self._counters[name] = handles

    def _read(self, counter: ctypes.c_void_p) -> int:
        value = _CounterValue()
        _check(
            self._pdh.PdhGetFormattedCounterValue(
                counter, _PDH_FMT_LARGE, None, ctypes.byref(value)
            ),
            "PdhGetFormattedCounterValue",
        )
        return max(0, int(value.value.largeValue))

    def _close(self) -> None:
        if self._pdh is not None and self._query is not None:
            self._pdh.PdhCloseQuery(self._query)
        self._query = None
        self._counters = {}


def _check(status: int, action: str) -> None:
    if status != 0:
        raise OSError(f"{action} failed with PDH status 0x{status & 0xFFFFFFFF:08X}")
