# Imports
import tkinter as tk
import notification_properties as np
import events
import utils


class BaseNotification(tk.Tk):
    def __init__(self, width: int = 350, height: int = 125, alpha: float = 1.0,
                 hAlign: np.HAlignment = np.HAlignment.RIGHT, vAlign: np.VAlignment = np.VAlignment.TOP,
                 fixedHPosition: int = 0, fixedVPosition: int = 0, hMargin: int = 15, vMargin: int = 15,
                 timeout: float = 3.0, alwaysOnTop: bool = True, destroyOnCloseEvent: bool = True,
                 closeOnTimeout: bool = True, tickResolution: int = 40, **kwargs):
        # Init the window
        tk.Tk.__init__(self)

        # Our event system
        self.eventManager = events.EventManager()
        self.destroyOnCloseEvent = destroyOnCloseEvent
        self.closeOnTimeout = closeOnTimeout
        self.tickResolution = tickResolution
        self.timeout = timeout
        self.timeoutTimer = 0.0
        self.timeoutTimerRunning = True
        self.lastTickTime = 0
        self.notificationOpened = False
        self.isHoveringOn = False
        self.didTimeout = False

        # Remove window border
        self.wm_overrideredirect(True)
        # Set transparency
        self.attributes("-alpha", alpha)
        # Set always on top
        self.attributes("-topmost", alwaysOnTop)

        # Set the size of the notification window
        self.geometry(f"{width}x{height}")

        # Bind any click event on the window
        self.bind("<Button-1>", self.on_notification_clicked)

        # Bind hover on/off events on the window
        self.bind("<Enter>", self.on_hover_on)
        self.bind("<Leave>", self.on_hover_off)

        # Update notification placement
        self.update_alignment(hAlign, vAlign, hMargin=hMargin, vMargin=vMargin,
                              fixedHPosition=fixedHPosition, fixedVPosition=fixedVPosition)

    def show_notification(self) -> None:
        # Set timeout timer
        self.timeoutTimer = 0.0

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

    def on_hover_on(self, event=None) -> None:
        # For some reason, tkinter emits this event twice...
        if self.isHoveringOn:
            return
        # Emit to listeners
        self.isHoveringOn = True
        self.eventManager.emit(np.EVENT_HOVER_ON, self)

    def on_hover_off(self, event=None) -> None:
        # For some reason, tkinter emits this event twice...
        if not self.isHoveringOn:
            return
        # Emit to listeners
        self.isHoveringOn = False
        self.eventManager.emit(np.EVENT_HOVER_OFF, self)

    def emit_notification_open(self) -> None:
        # Emit to listeners
        self.eventManager.emit(np.EVENT_OPEN, self)
        # Begin ticking for the first time
        self.lastTickTime = utils.current_time_millis()
        self.after(self.tickResolution, self.emit_notification_tick)
        # Indiciate that "open" has run
        self.notificationOpened = True

    def emit_notification_tick(self) -> None:
        curTime: int = utils.current_time_millis()
        delta: float = float(curTime - self.lastTickTime) / 1000.0
        self.lastTickTime = curTime

        # Do our own update for the timeout timer
        if self.timeoutTimerRunning:
            self.timeoutTimer += delta
            if self.timeoutTimer >= self.timeout and not self.didTimeout:
                self.didTimeout = True
                self.emit_notification_timeout()

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


class SimpleTextNotification(BaseNotification):
    def __init__(self, text: str, backgroundColor: str = "#333333", textColor: str = "#ffffff",
                 closeOnClick: bool = False, fontName: str = "Courier", fontSize: int = 12,
                 hoverBackgroundColor: str = "#666666", hoverTextColor: str = "#ffffff",
                 resetTimeoutOnHover: bool = True, borderSize: int = 2, borderColor: str = "#ffffff",
                 borderRelief: str = "flat", cursor: str = "arrow", hoverBorderColor: str = "#999999", **kwargs):
        BaseNotification.__init__(self, **kwargs)

        # Save colors
        self.backgroundColor = backgroundColor
        self.hoverBackgroundColor = hoverBackgroundColor
        self.textColor = textColor
        self.hoverTextColor = hoverTextColor
        self.borderColor = borderColor
        self.hoverBorderColor = hoverBorderColor
        self.resetTimeoutOnHover = resetTimeoutOnHover

        # The frame / border decoration
        self.frame = tk.Frame(self, bd=0, highlightbackground=self.borderColor, highlightcolor=self.borderColor,
                              highlightthickness=borderSize, relief=borderRelief, cursor=cursor)
        self.frame.pack_propagate(0)
        self.frame.pack(fill=tk.BOTH, expand=1)

        # The text label
        self.label = tk.Label(
            self.frame, text=text, bg=self.backgroundColor, fg=self.textColor, wraplength=self.winfo_width())
        self.label.config(font=(fontName, fontSize))
        self.label.pack(fill=tk.BOTH, expand=1)

        # Hover handlers
        self.on(np.EVENT_HOVER_ON, self.set_hover_style)
        self.on(np.EVENT_HOVER_OFF, self.set_normal_style)

        # Setup close on click
        if closeOnClick:
            self.on(np.EVENT_CLICKED, self.perform_close)

    def perform_close(self, notification: BaseNotification):
        self.emit_notification_close()

    def set_hover_style(self, notification: BaseNotification):
        self.label.config(bg=self.hoverBackgroundColor, fg=self.hoverTextColor)
        self.frame.config(highlightbackground=self.hoverBorderColor,
                          highlightcolor=self.hoverBorderColor)
        if self.resetTimeoutOnHover:
            self.timeoutTimerRunning = False
            self.timeoutTimer = 0.0

    def set_normal_style(self, notification: BaseNotification):
        self.label.config(bg=self.backgroundColor, fg=self.textColor)
        self.frame.config(highlightbackground=self.borderColor,
                          highlightcolor=self.borderColor)
        if self.resetTimeoutOnHover:
            self.timeoutTimer = 0.0
            self.timeoutTimerRunning = True


class SimpleTextNotificationWithTimeoutBar(SimpleTextNotification):
    def __init__(self, text: str, timeoutBarHeight: int = 3, timeoutBarBackgroundColor: str = "#ff0000",
                 timeoutBarForegroundColor: str = "#00ff00", **kwargs):
        SimpleTextNotification.__init__(self, text, **kwargs)

        self.timeoutCanvas = tk.Canvas(
            self.frame, height=timeoutBarHeight, highlightthickness=0)
        self.timeoutCanvas.pack(fill=tk.X, side=tk.BOTTOM, expand=0)

        self.update_idletasks()

        self.timeoutBarBackground = self.timeoutCanvas.create_rectangle(
            0, 0, self.timeoutCanvas.winfo_width(), self.timeoutCanvas.winfo_height(), fill=timeoutBarBackgroundColor)
        self.timeoutBarForeground = self.timeoutCanvas.create_rectangle(
            0, 0, 0, self.timeoutCanvas.winfo_height(), fill=timeoutBarForegroundColor)

        self.on(np.EVENT_TICK, self.update_timeout_progress_bar)

    def update_timeout_progress_bar(self, notification: BaseNotification, delta: float):
        self.timeoutCanvas.coords(self.timeoutBarForeground, 0, 0,
                                  int(self.timeoutTimer / self.timeout *
                                      self.timeoutCanvas.winfo_width()),
                                  self.timeoutCanvas.winfo_height())
