# Imports
import tkinter as tk
from enum import Enum
import time
from .event_manager import *

EVENT_BEFORE_OPEN: str = "before_open"  # notification
EVENT_OPEN: str = "open"  # notification
EVENT_CLOSE: str = "close"  # notification
EVENT_CLICKED: str = "clicked"  # notification
EVENT_HOVER_ON: str = "hover_on"  # notification
EVENT_HOVER_OFF: str = "hover_off"  # notification
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


class BaseNotification(tk.Tk):
    def __init__(self, width: int = 350, height: int = 125, alpha: float = 1.0,
                 hAlign: HAlignment = HAlignment.RIGHT, vAlign: VAlignment = VAlignment.TOP,
                 fixedHPosition: int = 0, fixedVPosition: int = 0, hMargin: int = 15, vMargin: int = 15,
                 timeout: float = 3.0, alwaysOnTop: bool = True, destroyOnCloseEvent: bool = True,
                 tickResolution: int = 33, borderSize: int = 2, borderColor: str = "#666666",
                 borderRelief: str = "flat", cursor: str = "arrow", **kwargs):
        # Init the window
        tk.Tk.__init__(self)

        # Variables to store
        self.eventManager = EventManager()
        self.destroyOnCloseEvent = destroyOnCloseEvent
        self.tickResolution = tickResolution
        self.timeout = timeout

        # Standard variables
        self.lastTickTime = 0
        self.timeoutTimer = 0.0
        self.timeoutTimerRunning = True
        self.shown = False
        self.openEmitted = False
        self.closeEmitted = False
        self.destroyed = False
        self.didTimeout = False
        self.isHoveringOn = False
        self.components = []
        self.afterIds = []

        # Remove window border
        self.wm_overrideredirect(True)
        # Set transparency
        self.attributes("-alpha", alpha)
        # Set always on top
        self.attributes("-topmost", alwaysOnTop)

        # Set the size of the notification window
        self.geometry(f"{width}x{height}")

        # The frame / border decoration
        self.frame = tk.Frame(self, bd=0, highlightbackground=borderColor, highlightcolor=borderColor,
                              highlightthickness=borderSize, relief=borderRelief, cursor=cursor)
        self.frame.pack_propagate(0)
        self.frame.pack(fill=tk.BOTH, expand=1)

        # Bind any click event on the window
        self.bind("<Button-1>", self.on_notification_clicked)

        # Bind hover on/off events on the window
        self.bind("<Enter>", self.on_hover_on)
        self.bind("<Leave>", self.on_hover_off)

        # Update notification placement
        self.update_alignment(hAlign, vAlign, hMargin=hMargin, vMargin=vMargin,
                              fixedHPosition=fixedHPosition, fixedVPosition=fixedVPosition)

    def show_notification(self) -> None:
        # Can't show the same notification twice
        if self.shown:
            raise BaseException(
                "Cannot show the same notification more than once.")
        self.shown = True

        # Set timeout timer
        self.timeoutTimer = 0.0

        # Run the pre-open events
        self.eventManager.emit(EVENT_BEFORE_OPEN, self)

        # Run the open event immediately as it starts
        self.make_after(0, self.emit_notification_open)
        self.mainloop()

    def on_notification_clicked(self, event=None) -> None:
        # Emit to listeners
        self.eventManager.emit(EVENT_CLICKED, self)

    def on_hover_on(self, event=None) -> None:
        # For some reason, tkinter emits this event twice...
        if self.isHoveringOn:
            return
        # Emit to listeners
        self.isHoveringOn = True
        self.eventManager.emit(EVENT_HOVER_ON, self)

    def on_hover_off(self, event=None) -> None:
        # For some reason, tkinter emits this event twice...
        if not self.isHoveringOn:
            return
        # Emit to listeners
        self.isHoveringOn = False
        self.eventManager.emit(EVENT_HOVER_OFF, self)

    def emit_notification_open(self) -> None:
        # Only if not already done
        if self.openEmitted:
            return
        self.openEmitted = True
        # Emit to listeners
        self.eventManager.emit(EVENT_OPEN, self)
        # Begin ticking for the first time
        self.lastTickTime = int(round(time.time() * 1000))
        self.make_after(self.tickResolution, self.emit_notification_tick)

    def emit_notification_tick(self) -> None:
        # Calculate delta time
        curTime: int = int(round(time.time() * 1000))
        delta: float = float(curTime - self.lastTickTime) / 1000.0
        self.lastTickTime = curTime

        # Do our own update for the timeout timer
        if self.timeoutTimerRunning:
            self.timeoutTimer += delta
            if self.timeoutTimer >= self.timeout and not self.didTimeout:
                self.emit_notification_close()

        # If the above exited the app, stop here
        if self.destroyed:
            return

        # Emit the tick event, and re-start the ticker, if we're not closed
        self.eventManager.emit(EVENT_TICK, self, delta)
        # Re-start the next ticker cycle
        self.make_after(self.tickResolution, self.emit_notification_tick)

    def emit_notification_close(self) -> None:
        # Only if not already done
        if self.closeEmitted:
            return
        self.closeEmitted = True
        # Emit to listeners
        self.eventManager.emit(EVENT_CLOSE, self)
        # Close ourselves if we are set to
        if self.destroyOnCloseEvent:
            self.destroy_now()

    def update_alignment(self, hAlign: HAlignment, vAlign: VAlignment, fixedHPosition: int = 0,
                         fixedVPosition: int = 0, hMargin: int = 0, vMargin: int = 0) -> None:
        # Ensure sizes are all updated for below calculations
        self.update_idletasks()

        # Horizontal alignment
        if hAlign == HAlignment.CENTER:
            xp = int((self.winfo_screenwidth() / 2) - (self.winfo_width() / 2))
        elif hAlign == HAlignment.LEFT:
            xp = hMargin
        elif hAlign == HAlignment.RIGHT:
            xp = int(self.winfo_screenwidth() -
                     self.winfo_width() - hMargin)
        else:
            xp = fixedHPosition

        # Vertical alignment
        if vAlign == VAlignment.CENTER:
            yp = int((self.winfo_screenheight() / 2) -
                     (self.winfo_height() / 2))
        elif vAlign == VAlignment.TOP:
            yp = vMargin
        elif vAlign == VAlignment.BOTTOM:
            yp = int(self.winfo_screenheight() -
                     self.winfo_height() - vMargin)
        else:
            yp = fixedVPosition

        # Actually set the position
        self.geometry(f"+{xp}+{yp}")

    def add_component(self, component) -> None:
        if component in self.components:
            raise BaseException(
                "Cannot add the same component more than once to a notification.")
        self.components.append(component)
        component.bind(self)

    def make_after(self, waitMillis: int, func: callable, *args) -> None:
        self.afterIds.append(self.after(waitMillis, func, *args))

    def destroy_now(self) -> None:
        # Only if not destroyed
        if self.destroyed:
            return
        self.destroyed = True
        # Remove all after callbacks (due to a weird bug with multiple notifications)
        for afterId in self.afterIds:
            self.after_cancel(afterId)
        # Then destroy the app
        self.destroy()

    def on(self, eventName: str, callback: callable) -> None:
        self.eventManager.on(eventName, callback)

    def remove_on(self, eventName: str, callback: callable) -> None:
        self.eventManager.remove_on(eventName, callback)


class TextNotification(BaseNotification):
    def __init__(self, text: str, backgroundColor: str = "#333333", hoverBackgroundColor: str = "#111111",
                 textColor: str = "#ffffff", fontName: str = "Courier", fontSize: int = 12,
                 justify: str = tk.CENTER, **kwargs):
        # Super
        BaseNotification.__init__(self, **kwargs)

        # Create the label
        self.textLabel = tk.Label(self.frame, text=text, bg=backgroundColor,
                                  fg=textColor, wraplength=self.winfo_width(), justify=justify)
        self.textLabel.config(font=(fontName, fontSize))
        self.textLabel.pack(fill=tk.BOTH, expand=1)

        # Subscribe to hovers to change color
        self.on(EVENT_HOVER_ON, lambda notification: self.textLabel.config(
            bg=hoverBackgroundColor))
        self.on(EVENT_HOVER_OFF, lambda notification: self.textLabel.config(
            bg=backgroundColor))
