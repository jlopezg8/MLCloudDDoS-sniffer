from datetime import datetime
import re

Interface = str


def get_flow_filename(interface: Interface):
    interface = re.sub(r'[^\w{}]', '-', interface, flags=re.ASCII)
    timestamp = f'{datetime.now():%Y-%m-%dT%H-%M-%S}'
    return f'capture_{interface}_{timestamp}.csv'
