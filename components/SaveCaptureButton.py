from __future__ import annotations

from collections.abc import Callable

import tkinter as tk
from tkinter import filedialog, ttk

from components.events import Event
from services import SnifferProtocol
from services.get_capture_filename import Interface


class SaveCaptureButton(ttk.Button):
    def __init__(
        self,
        master: tk.Misc,
        *,
        get_capture_filename: Callable[[Interface], str],
        interface_var: tk.StringVar,
        sniffer: SnifferProtocol,
    ):
        # TODO: create two buttons: one to save as JSON, the other one to save
        # as flow CSV:
        super().__init__(
            master,
            text='Guardar captura',
            command=self._save_capture_as_flow_csv,
            state='disabled',
            width=15,
        )
        self._get_capture_filename = get_capture_filename
        self._interface_var = interface_var
        self._sniffer = sniffer
        self._the_root: tk.Tk = master._root()  # type: ignore
        self._bind_event_handlers()

    def _save_capture_as_json(self):
        options = dict(
            initialfile=self._get_capture_filename(self._interface_var.get()),
            filetypes=(
                ('JSON', '*.json'),
                ('Todos los archivos', '*'),
            ),
        )
        if (filename := filedialog.asksaveasfilename(**options)):
            self._sniffer.save_packets_as_json(filename)
    
    def _save_capture_as_flow_csv(self):
        options = dict(
            initialfile=self._get_capture_filename(self._interface_var.get()),
            filetypes=(
                ('CSV', '*.csv'),
                ('Todos los archivos', '*'),
            ),
        )
        if (filename := filedialog.asksaveasfilename(**options)):
            self._sniffer.save_packets_as_flow_csv(filename)

    def _bind_event_handlers(self):
        self._the_root.bind(
            Event.CAPTURE_STARTED,
            lambda event: self.configure(state='disabled'),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_ENDED,
            lambda event: self.configure(state='normal'),
            add=True,
        )
