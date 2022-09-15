import json
import tempfile
from threading import Thread

import pyshark
from cicflowmeter.sniffer import create_sniffer

from services.to_json_serializable import serialize


class Sniffer:
    def __init__(self):
        self._output_file = None
        self._capturing = False
        self._raw_packets = []
        self._serialized_packets = []

    def start_capture(self, interface: str):
        if not self._capturing:
            # A daemon thread so that it doesn't stop the Python program from
            # exiting:
            (Thread(target=self._start_capture, args=(interface,), daemon=True)
                .start())

    def _start_capture(self, interface: str):
        self._output_file = 'asdf.pcap'#tempfile.mktemp()  # TODO: use something else
        with pyshark.LiveCapture(interface or None, output_file=self._output_file)\
             as sniffer:
            self._capturing = True
            self._raw_packets = []
            self._serialized_packets = []
            for packet in sniffer.sniff_continuously():
                if not self._capturing:
                    break
                self._raw_packets.append(packet)
                self._serialized_packets.append(serialize(packet))

    def stop_capture(self):
        if self._capturing:
            self._capturing = False

    def get_packets(self):
        return self._serialized_packets

    def save_packets_as_json(self, filename):
        with open(filename, 'wt') as file:
            json.dump(self._serialized_packets, file)
    
    def save_packets_as_flow_csv(self, filename):
        sniffer = create_sniffer(
            input_file=self._output_file,
            input_interface=None,
            output_mode='flow',
            output_file=filename,
        )
        sniffer.start()
        sniffer.join()
