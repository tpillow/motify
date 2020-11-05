# Imports
import tkinter as tk
from typing import Tuple
from .notifications import *


class TimeoutProgressBarComponent():
    def __init__(self, timeoutBarHeight: int = 3, timeoutBarBackgroundColor: str = "#ff0000",
                 timeoutBarForegroundColor: str = "#00ff00"):
        self.timeoutBarHeight = timeoutBarHeight
        self.timeoutBarBackgroundColor = timeoutBarBackgroundColor
        self.timeoutBarForegroundColor = timeoutBarForegroundColor

    def bind(self, notification: BaseNotification) -> None:
        # It's up to the implementer to pack the timeoutCanvas appropriately
        self.canvas = tk.Canvas(
            notification.frame, height=self.timeoutBarHeight, highlightthickness=0)

        # Events to setup the bars and update them throughout
        notification.on(EVENT_OPEN, self.create_timeout_bars)
        notification.on(EVENT_TICK, self.update_timeout_progress_bar)

    def create_timeout_bars(self, notification: BaseNotification) -> None:
        # Create the actual canvas items at the current width / heights
        self.timeoutBarBackground = self.canvas.create_rectangle(
            0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=self.timeoutBarBackgroundColor)
        self.timeoutBarForeground = self.canvas.create_rectangle(
            0, 0, 0, self.canvas.winfo_height(), fill=self.timeoutBarForegroundColor)

    def update_timeout_progress_bar(self, notification: BaseNotification, delta: float) -> None:
        self.canvas.coords(self.timeoutBarForeground, 0, 0,
                           int(notification.timeoutTimer / notification.timeout *
                               self.canvas.winfo_width()),
                           self.canvas.winfo_height())
