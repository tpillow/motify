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


class ContextMenuComponent():
    def __init__(self, menuOpts: list[tuple]):
        # List of (Str, Callable)
        self.menuOpts = menuOpts

    def bind(self, notification: BaseNotification) -> None:
        # Save the notification for use
        self.notification = notification

        # Create the menu
        self.menu = tk.Menu(notification.frame, tearoff=0)
        for opt in self.menuOpts:
            self.menu.add_command(label=opt[0], command=opt[1])
        notification.bind("<Button-3>", self.show_menu)

    def show_menu(self, event=None) -> None:
        # We have to stop the timeout timer from closing the widget
        oldTimerRunning = self.notification.timeoutTimerRunning
        self.notification.timeoutTimerRunning = False

        # Display the menu and close it properly
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

        # Re-enable the timeout timer to it's previous state
        self.notification.timeoutTimerRunning = oldTimerRunning
