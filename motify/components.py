# Imports
import tkinter as tk
from typing import Tuple
from .notifications import *


class ButtonComponent():
    def __init__(self, btnDefs: list[Tuple[str, callable]], padx: int = 10, pady: int = 0, marginx: int = 5,
                 backgroundColor: str = "#333333"):
        self.btnDefs = btnDefs
        self.padx = padx
        self.pady = pady
        self.marginx = marginx
        self.backgroundColor = backgroundColor
        self.btns = []

    def bind(self, notification: BaseNotification):
        self.frame = tk.Frame(notification.frame, bg=self.backgroundColor)
        self.frame.pack(fill=tk.X, side=tk.BOTTOM)

        for btnDef in self.btnDefs:
            btn = tk.Button(self.frame,
                            text=btnDef[0], command=btnDef[1], padx=self.padx, pady=self.pady)
            btn.pack(side=tk.RIGHT, padx=self.marginx)
            self.btns.append(btn)


class TextComponent():
    def __init__(self, text: str, backgroundColor: str = "#333333", textColor: str = "#ffffff",
                 fontName: str = "Courier", fontSize: int = 12, justify: str = tk.CENTER,
                 fill: str = tk.BOTH, expand: float = 1):
        self.text = text
        self.backgroundColor = backgroundColor
        self.textColor = textColor
        self.fontName = fontName
        self.fontSize = fontSize
        self.justify = justify
        self.fill = fill
        self.expand = expand

    def bind(self, notification: BaseNotification) -> None:
        # The text label
        self.label = tk.Label(
            notification.frame, text=self.text, bg=self.backgroundColor, fg=self.textColor, wraplength=notification.winfo_width(), justify=self.justify)
        self.label.config(font=(self.fontName, self.fontSize))
        self.label.pack(fill=self.fill, expand=self.expand)


class TimeoutProgressBarComponent():
    def __init__(self, timeoutBarHeight: int = 3, timeoutBarBackgroundColor: str = "#ff0000",
                 timeoutBarForegroundColor: str = "#00ff00"):
        self.timeoutBarHeight = timeoutBarHeight
        self.timeoutBarBackgroundColor = timeoutBarBackgroundColor
        self.timeoutBarForegroundColor = timeoutBarForegroundColor

    def bind(self, notification: BaseNotification) -> None:
        self.timeoutCanvas = tk.Canvas(
            notification.frame, height=self.timeoutBarHeight, highlightthickness=0)
        self.timeoutCanvas.pack(fill=tk.X, side=tk.BOTTOM, expand=0)

        notification.update_idletasks()

        self.timeoutBarBackground = self.timeoutCanvas.create_rectangle(
            0, 0, self.timeoutCanvas.winfo_width(), self.timeoutCanvas.winfo_height(), fill=self.timeoutBarBackgroundColor)
        self.timeoutBarForeground = self.timeoutCanvas.create_rectangle(
            0, 0, 0, self.timeoutCanvas.winfo_height(), fill=self.timeoutBarForegroundColor)

        notification.on(EVENT_TICK, self.update_timeout_progress_bar)

    def update_timeout_progress_bar(self, notification: BaseNotification, delta: float):
        self.timeoutCanvas.coords(self.timeoutBarForeground, 0, 0,
                                  int(notification.timeoutTimer / notification.timeout *
                                      self.timeoutCanvas.winfo_width()),
                                  self.timeoutCanvas.winfo_height())
