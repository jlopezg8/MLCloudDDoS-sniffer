import tkinter as tk
from tkinter import ttk

from components.events import Event
from services import SnifferProtocol


class StartStopCaptureButton(ttk.Button):
    _START_CAPTURE_TEXT = 'Iniciar captura'
    _STOP_CAPTURE_TEXT = 'Detener captura'

    def __init__(
        self,
        master: tk.Misc,
        *,
        sniffer: SnifferProtocol,
        interface_var: tk.StringVar,
    ):
        super().__init__(
            master,
            text=self._START_CAPTURE_TEXT,
            command=self._start_capture,
            state='disabled',
            width=15,
        )
        self._sniffer = sniffer
        self._interface_var = interface_var
        self._the_root: tk.Tk = master._root()  # type: ignore
        self._bind_event_handlers()

    def _start_capture(self):
        self._sniffer.start_capture(interface=self._interface_var.get())
        self._the_root.event_generate(Event.CAPTURE_STARTED)

    def _stop_capture(self):
        self._sniffer.stop_capture()
        self._the_root.event_generate(Event.CAPTURE_ENDED)

    def _bind_event_handlers(self):
        self._the_root.bind(
            Event.INTERFACE_SELECTED,
            lambda event: self.configure(
                state='normal' if self._interface_var.get() else 'disabled',
            ),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_STARTED,
            lambda event: self.configure(
                text=self._STOP_CAPTURE_TEXT,
                command=self._stop_capture,
            ),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_ENDED,
            lambda event: self.configure(
                text=self._START_CAPTURE_TEXT,
                command=self._start_capture,
            ),
            add=True,
        )
