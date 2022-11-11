import os
import tempfile
from threading import Thread

import pyshark
import cicflowmeter.sniffer

from services.SnifferProtocol import SnifferProtocol


class Sniffer(SnifferProtocol):
    def __init__(self):
        self._capturing = False
        self._capture_filepath = None

    def start_capture(self, interface: str):
        self._validate_not_capturing()
        # For some reason this has to be done outside of the threaded function:
        # See (There is no current event loop in thread 'Thread-8'. · Issue #611 · KimiNewt/pyshark)
        # [https://github.com/KimiNewt/pyshark/issues/611]
        self._init_sniffer(interface)
        # A daemon thread so that it doesn't stop the Python program from
        # exiting:
        Thread(target=self._start_capture, daemon=True).start()

    def _validate_not_capturing(self):
        if self._capturing:
            raise RuntimeError(
                'a capture is already in progress;'
                + ' stop the capture first using `sniffer.stop_capture()`'
            )

    def _init_sniffer(self, interface):
        self._capture_filepath = tempfile.mktemp()  # TODO: use something else
        self._sniffer = pyshark.LiveCapture(
            interface,
            output_file=self._capture_filepath,
        )

    def _start_capture(self):
        with self._sniffer:
            self._capturing = True
            for _ in self._sniffer.sniff_continuously():
                if not self._capturing:
                    break

    def stop_capture(self):
        self._capturing = False

    def save_capture_as_flow(self, flow_filepath: str):
        self._validate_not_capturing()
        if not self._capture_filepath:
            raise RuntimeError('a capture has to be made first')
        self._convert_capture_to_flow(flow_filepath)
        self._clear_capture()

    def _convert_capture_to_flow(self, flow_filepath):
        # Adapted from https://gitlab.com/hieulw/cicflowmeter/-/blob/master/src/cicflowmeter/sniffer.py#L80:
        sniffer = cicflowmeter.sniffer.create_sniffer(
            input_file=self._capture_filepath,
            input_interface=None,
            output_mode='flow',
            output_file=flow_filepath,
        )
        sniffer.start()
        sniffer.join()

    def _clear_capture(self):
        assert self._capture_filepath is not None
        os.remove(self._capture_filepath)
        self._capture_filepath = None
