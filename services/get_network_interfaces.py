from __future__ import annotations

import platform

InterfaceFriendlyName = str
InterfaceName = str


def get_network_interfaces() -> dict[InterfaceFriendlyName, InterfaceName]:
    if platform.system() == 'Windows':
        # https://stackoverflow.com/a/53012414/10150433
        from scapy.arch.windows import get_windows_if_list
        return {
            # tshark on Windows expects interfaces in this format:
            interface['name']: fr'\Device\NPF_{interface["guid"]}'
            for interface in get_windows_if_list()
            if interface['ips']  # to filter out irrelevant interfaces
        }

    else:
        import netifaces
        return {interface: interface for interface in netifaces.interfaces()}


def main():
    from pprint import pprint    
    pprint(get_network_interfaces())


if __name__ == '__main__':
    main()
