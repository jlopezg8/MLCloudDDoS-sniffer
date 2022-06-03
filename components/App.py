from __future__ import annotations

import tkinter as tk
from collections.abc import Callable, Mapping
from tkinter import ttk

from components.CaptureViewer import CaptureViewer
from components.InterfaceDropdown import InterfaceDropdown
from components.SaveCaptureButton import SaveCaptureButton
from components.StartStopCaptureButton import StartStopCaptureButton
from services import SnifferProtocol
from services.get_capture_filename import Interface
from services.get_network_interfaces import (
    InterfaceFriendlyName, InterfaceName)


class App(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        network_interfaces: Mapping[InterfaceFriendlyName, InterfaceName],
        sniffer: SnifferProtocol,
        get_capture_filename: Callable[[Interface], str],
    ):
        super().__init__(master, padding=10)
        self._network_interfaces = network_interfaces
        self._sniffer = sniffer
        self._get_capture_filename = get_capture_filename
        self._interface_var = tk.StringVar()
        self._the_root: tk.Tk = self._root()  # type: ignore
        self._create_widgets()
        self._bind_event_handlers()

    def _create_widgets(self):
        PADDING_Y = (10, 0)  # padding-top: 10px
        InterfaceDropdown(
            self,
            network_interfaces=self._network_interfaces,
            interface_var=self._interface_var,
        ).pack(expand=True, fill=tk.X)
        StartStopCaptureButton(
            self,
            sniffer=self._sniffer,
            interface_var=self._interface_var,
        ).pack(pady=PADDING_Y)
        CaptureViewer(
            self,
            sniffer=self._sniffer,
        ).pack(expand=True, fill=tk.BOTH, pady=PADDING_Y)
        SaveCaptureButton(
            self,
            get_capture_filename=self._get_capture_filename,
            interface_var=self._interface_var,
            sniffer=self._sniffer,
        ).pack(pady=PADDING_Y)

    def _bind_event_handlers(self):
        self._the_root.protocol('WM_DELETE_WINDOW', self._on_wm_delete_window)

    def _on_wm_delete_window(self):
        self._sniffer.stop_capture()
        self._the_root.destroy()
