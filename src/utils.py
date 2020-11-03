# Imports
import time


def current_time_millis() -> int:
    """Gets the current system time in milliseconds.

    Returns:
        int: current time (milliseconds)
    """
    return int(round(time.time() * 1000))
