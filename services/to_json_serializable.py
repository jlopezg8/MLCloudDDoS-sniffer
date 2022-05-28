from typing import Any


def serialize(o: Any):
    if isinstance(o, dict):
        return {key: serialize(value) for (key, value) in o.items()}
    elif isinstance(o, (list, tuple)):
        return [serialize(e) for e in o]
    elif isinstance(o, str):
        return o
    elif hasattr(o, '__dict__'):
        return {key: serialize(value) for (key, value) in o.__dict__.items()}
    else:
        return repr(o)
