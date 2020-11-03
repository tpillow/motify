from enum import Enum

EVENT_BEFORE_OPEN: str = "before_open"  # notification
EVENT_OPEN: str = "open"  # notification
EVENT_TIMEOUT: str = "timeout"  # notification
EVENT_CLOSE: str = "close"  # notification
EVENT_CLICKED: str = "clicked"  # notification
EVENT_TICK: str = "tick"  # notification, delta: float


class HAlignment(Enum):
    """Represents horizontal alignment.
    """
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    FIXED = 4


class VAlignment(Enum):
    """Represents vertical alignment.
    """
    BOTTOM = 1
    CENTER = 2
    TOP = 3
    FIXED = 4
