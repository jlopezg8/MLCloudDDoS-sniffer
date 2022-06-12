from __future__ import annotations

import tkinter as tk
from collections.abc import Mapping
from tkinter import ttk

from components.events import Event
from services.get_network_interfaces import (
    InterfaceFriendlyName, InterfaceName)


class InterfaceDropdown(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        network_interfaces: Mapping[InterfaceFriendlyName, InterfaceName],
        interface_var: tk.StringVar,
    ):
        super().__init__(master)
        self._network_interfaces = network_interfaces
        self._interface_var = interface_var
        self._interface_friendly_name_var = tk.StringVar()
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
            textvariable=self._interface_friendly_name_var,
            values=list(self._network_interfaces.keys()),
        )
        self._combobox.pack(expand=True, fill=tk.X)

    def _bind_event_handlers(self):
        self._combobox.bind(
            '<<ComboboxSelected>>',
            self._on_combobox_selected,
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_STARTED,
            lambda event: self._combobox.configure(state='disabled'),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_ENDED,
            lambda event: self._combobox.configure(state='normal'),
            add=True,
        )
    
    def _on_combobox_selected(self, event: tk.Event[ttk.Combobox]):
        interface_friendly_name = self._interface_friendly_name_var.get()
        interface = self._network_interfaces[interface_friendly_name]
        self._interface_var.set(interface)
        
        self._the_root.event_generate(Event.INTERFACE_SELECTED)
