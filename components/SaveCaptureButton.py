import re
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, ttk

from components.events import Event
from services import SnifferProtocol


class SaveCaptureButton(ttk.Button):
    def __init__(
        self,
        master: tk.Misc,
        *,
        sniffer: SnifferProtocol,
        interface_var: tk.StringVar,
    ):
        super().__init__(
            master,
            text='Guardar captura',
            command=self._save_capture,
            state='disabled',
            width=15,
        )
        self._sniffer = sniffer
        self._interface_var = interface_var
        self._the_root: tk.Tk = master._root()  # type: ignore
        self._bind_event_handlers()

    def _save_capture(self):
        options = dict(
            initialfile=self._get_capture_filename(),
            filetypes=(
                ('JSON', '*.json'),
                ('Todos los archivos', '*'),
            ),
        )
        if (filename := filedialog.asksaveasfilename(**options)):
            self._sniffer.save_packets_as_json(filename)

    def _get_capture_filename(self):
        """TODO: move to a new service? Is it worth it?"""
        interface = re.sub(r'[^a-zA-Z0-9{}]', '-', self._interface_var.get())
        timestamp = f'{datetime.now():%Y-%m-%dT%H-%M-%S}'
        return f'capture_{interface}_{timestamp}.json'

    def _bind_event_handlers(self):
        self._the_root.bind(
            Event.CAPTURE_STARTED,
            lambda event: self.config(state='disabled'),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_ENDED,
            lambda event: self.config(state='normal'),
            add=True,
        )
