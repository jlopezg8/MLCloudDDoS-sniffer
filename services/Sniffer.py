import json
from threading import Thread

import pyshark

from services.to_json_serializable import serialize


class Sniffer:
    def __init__(self):
        self._capturing = False
        self._packets = []

    def start_capture(self, interface: str):
        if not self._capturing:
            Thread(target=self._start_capture, args=(interface,)).start()

    def _start_capture(self, interface: str):
        with pyshark.LiveCapture(interface) as sniffer:
            self._capturing = True
            self._packets = []
            for packet in sniffer.sniff_continuously():
                self._packets.append(serialize(packet))
                if not self._capturing:
                    break

    def stop_capture(self):
        if self._capturing:
            self._capturing = False

    def get_packets(self):
        return self._packets

    def save_packets_as_json(self, filename):
        with open(filename, 'wt') as file:
            json.dump(self._packets, file)
