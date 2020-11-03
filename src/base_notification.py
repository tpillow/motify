# Imports
import tkinter as tk
import notification_properties as np
import events
import utils


class BaseNotification(tk.Tk):
    def __init__(self, width: int = 350, height: int = 125, alpha: float = 0.75,
                 hAlign: np.HAlignment = np.HAlignment.RIGHT, vAlign: np.VAlignment = np.VAlignment.TOP,
                 fixedHPosition: int = 0, fixedVPosition: int = 0, hMargin: int = 15, vMargin: int = 15,
                 timeout: int = 3000, alwaysOnTop: bool = True, destroyOnCloseEvent: bool = True,
                 closeOnTimeout: bool = True, tickEnabled: bool = False, tickResolution: int = 40):
        # Init the window
        tk.Tk.__init__(self)

        # Our event system
        self.eventManager = events.EventManager()
        self.destroyOnCloseEvent = destroyOnCloseEvent
        self.closeOnTimeout = closeOnTimeout
        self.tickEnabled = tickEnabled
        self.tickResolution = tickResolution
        self.lastTickTime = 0
        self.notificationOpened = False

        # Set any properties we need later
        self.timeout = timeout

        # Remove window border
        self.wm_overrideredirect(True)
        # Set transparency
        self.attributes("-alpha", alpha)
        # Set always on top
        self.attributes("-topmost", alwaysOnTop)

        # Create the main canvas
        self.geometry(f"{width}x{height}")
        self.mainFrame = tk.Frame(self, bg="red")
        # Prevent children from determining size
        self.mainFrame.pack_propagate(0)
        self.mainFrame.pack(fill=tk.BOTH, expand=1)

        # Binds
        self.bind('<Button-1>', self.on_notification_clicked)

        # Update notification placement
        self.update_alignment(hAlign, vAlign, hMargin=hMargin, vMargin=vMargin,
                              fixedHPosition=fixedHPosition, fixedVPosition=fixedVPosition)

    def show_notification(self) -> None:
        # Set timeout timer
        if self.timeout > 0:
            self.after(self.timeout, self.emit_notification_timeout)

        # Run the pre-open events
        self.eventManager.emit(np.EVENT_BEFORE_OPEN, self)

        # Run the open event immediately as it starts
        self.after(0, self.emit_notification_open)
        self.mainloop()

    def update_alignment(self, hAlign: np.HAlignment, vAlign: np.VAlignment, fixedHPosition: int = 0,
                         fixedVPosition: int = 0, hMargin: int = 0, vMargin: int = 0) -> None:
        # Ensure sizes are all updated for below calculations
        self.update_idletasks()

        # Horizontal alignment
        if hAlign == np.HAlignment.CENTER:
            xp = int((self.winfo_screenwidth() / 2) - (self.winfo_width() / 2))
        elif hAlign == np.HAlignment.LEFT:
            xp = hMargin
        elif hAlign == np.HAlignment.RIGHT:
            xp = int(self.winfo_screenwidth() -
                     self.winfo_width() - hMargin)
        else:
            xp = fixedHPosition

        # Vertical alignment
        if vAlign == np.VAlignment.CENTER:
            yp = int((self.winfo_screenheight() / 2) -
                     (self.winfo_height() / 2))
        elif vAlign == np.VAlignment.TOP:
            yp = vMargin
        elif vAlign == np.VAlignment.BOTTOM:
            yp = int(self.winfo_screenheight() -
                     self.winfo_height() - vMargin)
        else:
            yp = fixedVPosition

        # Actually set the position
        self.geometry(f"+{xp}+{yp}")

    def on_notification_clicked(self, event=None) -> None:
        # Emit to listeners
        self.eventManager.emit(np.EVENT_CLICKED, self)

    def emit_notification_open(self) -> None:
        # Emit to listeners
        self.eventManager.emit(np.EVENT_OPEN, self)
        # Begin ticking for the first time (if enabled)
        if self.tickEnabled:
            self.lastTickTime = utils.current_time_millis()
            self.after(self.tickResolution, self.emit_notification_tick)
        # Indiciate that "open" has run
        self.notificationOpened = True

    def setTickEnabled(self, enabled: bool) -> None:
        if (self.tickEnabled and enabled) or (not self.tickEnabled and not enabled):
            return  # No change in state
        if not self.tickEnabled and enabled:
            # Need to enable ticking (only if the window is shown)
            self.tickEnabled = True
            if self.notificationOpened:
                self.lastTickTime = utils.current_time_millis()
                self.after(self.tickResolution, self.emit_notification_tick)
        else:
            # Otherwise, disable ticking
            self.tickEnabled = False

    def emit_notification_tick(self) -> None:
        curTime: int = utils.current_time_millis()
        delta: float = float(curTime - self.lastTickTime) / 1000.0
        self.lastTickTime = curTime
        if self.tickEnabled:
            self.eventManager.emit(np.EVENT_TICK, self, delta)
            self.after(self.tickResolution, self.emit_notification_tick)

    def emit_notification_timeout(self) -> None:
        # Emit to listeners
        self.eventManager.emit(np.EVENT_TIMEOUT, self)
        # Close if we are set to
        if self.closeOnTimeout:
            self.emit_notification_close()

    def emit_notification_close(self) -> None:
        # Emit to listeners
        self.eventManager.emit(np.EVENT_CLOSE, self)
        # Close ourselves if we are set to
        if self.destroyOnCloseEvent:
            self.destroy()

    def on(self, eventName: str, callback: callable) -> None:
        self.eventManager.on(eventName, callback)

    def remove_on(self, eventName: str, callback: callable) -> None:
        self.eventManager.remove_on(eventName, callback)
