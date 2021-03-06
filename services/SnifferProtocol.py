from __future__ import annotations

from typing import Any, Protocol


class SnifferProtocol(Protocol):
    def start_capture(self, interface: str) -> None: ...
    def stop_capture(self) -> None: ...
    def get_packets(self) -> list[Any]: ...
    def save_packets_as_json(self, filename: str) -> None: ...
