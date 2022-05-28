from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from components.events import Event


class InterfaceDropdown(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        interface_var: tk.StringVar,
        network_interfaces: list[str],
    ):
        super().__init__(master)
        self._interface_var = interface_var
        self._network_interfaces = network_interfaces
        self._the_root: tk.Tk = self._root()  # type: ignore
        self._create_widgets()
        self._bind_event_handlers()

    def _create_widgets(self):
        ttk.Label(
            self,
            text='Interfaz',
            justify=tk.LEFT,
        ).pack(expand=True, fill=tk.X)
        self._combobox = ttk.Combobox(
            self,
            textvariable=self._interface_var,
            values=self._network_interfaces,
        )
        self._combobox.pack(expand=True, fill=tk.X)

    def _bind_event_handlers(self):
        self._combobox.bind(
            '<<ComboboxSelected>>',
            lambda event:
                self._the_root.event_generate(Event.INTERFACE_SELECTED),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_STARTED,
            lambda event: self._combobox.config(state='disabled'),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_ENDED,
            lambda event: self._combobox.config(state='normal'),
            add=True,
        )
