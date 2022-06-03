from datetime import datetime
import re

Interface = str


def get_capture_filename(interface: Interface):
    interface = re.sub(r'[^a-zA-Z0-9{}]', '-', interface)
    timestamp = f'{datetime.now():%Y-%m-%dT%H-%M-%S}'
    return f'capture_{interface}_{timestamp}.json'
