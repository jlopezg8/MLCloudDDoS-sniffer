import platform

import netifaces


def get_network_interfaces():
    interfaces: list[str] = netifaces.interfaces()
    if platform.system() == 'Windows':
        # TODO: explain this:
        return [fr'\\Device\\NPF_{interface}' for interface in interfaces]
    else:
        return interfaces
