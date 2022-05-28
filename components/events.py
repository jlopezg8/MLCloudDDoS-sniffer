from enum import Enum


class Event(str, Enum):
    INTERFACE_SELECTED = '<<InterfaceSelected>>'
    CAPTURE_STARTED = '<<CaptureStarted>>'
    CAPTURE_ENDED = '<<CaptureEnded>>'
