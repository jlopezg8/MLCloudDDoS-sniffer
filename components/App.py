from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from components.CaptureViewer import CaptureViewer
from components.InterfaceDropdown import InterfaceDropdown
from components.SaveCaptureButton import SaveCaptureButton
from components.StartStopCaptureButton import StartStopCaptureButton
from services import SnifferProtocol


class App(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        network_interfaces: list[str],
        sniffer: SnifferProtocol,
    ):
        super().__init__(master, padding=10)
        self._network_interfaces = network_interfaces
        self._sniffer = sniffer
        self._interface_var = tk.StringVar()
        self._the_root: tk.Tk = self._root()  # type: ignore
        self._create_widgets()
        self._bind_event_handlers()

    def _create_widgets(self):
        PADDING_Y = (10, 0)  # padding-top: 10px
        InterfaceDropdown(
            self,
            interface_var=self._interface_var,
            network_interfaces=self._network_interfaces,
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
            sniffer=self._sniffer,
            interface_var=self._interface_var,
        ).pack(pady=PADDING_Y)

    def _bind_event_handlers(self):
        self._the_root.protocol('WM_DELETE_WINDOW', self._on_wm_delete_window)

    def _on_wm_delete_window(self):
        self._sniffer.stop_capture()
        self._the_root.destroy()
