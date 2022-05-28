import tkinter as tk

from components import App
from services import get_network_interfaces, Sniffer


def main():
    root = tk.Tk()
    root.title('MLCloudDDoS Sniffer')
    App(
        root,
        network_interfaces=get_network_interfaces(),
        sniffer=Sniffer(),
    ).pack(expand=True, fill=tk.BOTH)
    root.mainloop()


if __name__ == '__main__':
    main()
