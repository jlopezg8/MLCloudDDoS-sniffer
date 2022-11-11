from __future__ import annotations

from collections.abc import Callable

import tkinter as tk
from tkinter import filedialog, ttk

from components.events import Event
from services import SnifferProtocol
from services.get_flow_filename import Interface


class SaveCaptureAsFlowButton(ttk.Button):
    def __init__(
        self,
        master: tk.Misc,
        *,
        get_flow_filename: Callable[[Interface], str],
        interface_var: tk.StringVar,
        sniffer: SnifferProtocol,
    ):
        super().__init__(
            master,
            text='Guardar captura',
            command=self._save_capture_as_flow,
            state='disabled',
            width=15,
        )
        self._get_flow_filename = get_flow_filename
        self._interface_var = interface_var
        self._sniffer = sniffer
        self._the_root: tk.Tk = master._root()  # type: ignore
        self._bind_event_handlers()

    def _save_capture_as_flow(self):
        options = dict(
            initialfile=self._get_flow_filename(self._interface_var.get()),
            filetypes=(
                ('CSV', '*.csv'),
                ('Todos los archivos', '*'),
            ),
        )
        if (flow_filepath := filedialog.asksaveasfilename(**options)):
            self._sniffer.save_capture_as_flow(flow_filepath)

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
