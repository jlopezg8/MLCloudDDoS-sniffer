from __future__ import annotations
import platform


def get_network_interfaces() -> dict[str, str]:
    if platform.system() == 'Windows':
        from winpcapy import WinPcapDevices
        return {
            description: name
            for name, description in WinPcapDevices.list_devices().items()}
    else:
        import netifaces
        return {interface: interface for interface in netifaces.interfaces()}
