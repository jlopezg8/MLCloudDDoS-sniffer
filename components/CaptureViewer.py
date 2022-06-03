import json
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import Any

from components.events import Event
from services.SnifferProtocol import SnifferProtocol


class CaptureViewer1(ScrolledText):
    def __init__(
        self,
        master: tk.Misc,
        *,
        sniffer: SnifferProtocol,
    ):
        super().__init__(
            master,
            width=55,
            height=25,
            #state='disabled',  # also disables event handling
        )
        self._sniffer = sniffer
        self._the_root: tk.Tk = self._root()  # type: ignore
        self._bind_event_handlers()

    def _bind_event_handlers(self):
        self._the_root.bind(
            Event.CAPTURE_STARTED,
            lambda event: self._set_text(''),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_ENDED,
            lambda event: self._set_text(
                json.dumps(self._sniffer.get_packets(), indent=2)
            ),
            add=True,
        )

    def _set_text(self, text: str):
        LINE_1_CHAR_0 = '1.0'
        self.delete(LINE_1_CHAR_0, tk.END)
        self.insert(LINE_1_CHAR_0, text)


class CaptureViewer2(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        sniffer: SnifferProtocol,
    ):
        super().__init__(master)
        self._sniffer = sniffer
        self._the_root: tk.Tk = self._root()  # type: ignore
        self._create_widgets()
        self._bind_event_handlers()

    def _create_widgets(self):
        self._treeview = ttk.Treeview(
            self,
            #width=55,  # No parameter named "width"
            height=19,
        )
        self._treeview.column('#0', width=443)
        self._treeview.pack(side=tk.LEFT)
        self._scrollbar = ttk.Scrollbar(
            self,
            command=self._treeview.yview,
            orient=tk.VERTICAL,
        )
        self._scrollbar.pack(expand=True, fill=tk.Y, side=tk.RIGHT)
        self._treeview.configure(yscrollcommand=self._scrollbar.set)

    def _bind_event_handlers(self):
        self._the_root.bind(
            Event.CAPTURE_STARTED,
            lambda event: self._clear(),
            add=True,
        )
        self._the_root.bind(
            Event.CAPTURE_ENDED,
            lambda event: self._show_capture(),
            add=True,
        )

    def _clear(self):
        for child in self._treeview.get_children():
            self._treeview.delete(child)

    def _show_capture(self):
        if (packets := self._sniffer.get_packets()):
            for i, packet in enumerate(packets, start=1):
                self._append_item(label=f'Paquete #{i}', item=packet)
        else:
            self._append_item(label='(Vacío)')

    def _append_item(self, label: str, item: Any = None, parent_id: str = ''):
        item_id = self._treeview.insert(
            parent=parent_id, index=tk.END, text=label, open=True)
        if isinstance(item, dict):
            for key, value in item.items():
                self._append_item(label=key, item=value, parent_id=item_id)
        elif isinstance(item, (list, tuple)):
            for i, e in enumerate(item, start=1):
                self._append_item(label=f'#{i}', item=e, parent_id=item_id)
        elif item is not None:
            self._treeview.insert(parent=item_id, index=tk.END, text=str(item))


def CaptureViewer(
    master: tk.Misc,
    *,
    sniffer: SnifferProtocol,
):
    frame = ttk.Frame(master)
    CaptureViewer1(frame, sniffer=sniffer).pack(side=tk.LEFT)
    CaptureViewer2(frame, sniffer=sniffer).pack(side=tk.RIGHT)
    return frame
