# Imports
import pytweening as tween
import utils
import notifications as bn
import notification_properties as np


class AlphaFadeInTransition():
    def __init__(self, duration: float = 1.0, startAlpha: float = 0.0,
                 endAlpha: float = 1.0, tweenFunc: callable = tween.linear):
        self.duration = duration
        self.startAlpha = startAlpha
        self.endAlpha = endAlpha
        self.tweenFunc = tweenFunc
        self.timer = 0.0
        self.bound = False

    def bind(self, notification: bn.BaseNotification) -> None:
        if self.bound:
            raise "Cannot bind the same transition to more than one notification"
        notification.on(np.EVENT_BEFORE_OPEN, self.before_open)
        self.bound = True

    def before_open(self, notification: bn.BaseNotification) -> None:
        self.timer = 0.0
        notification.attributes("-alpha", self.startAlpha)
        notification.on(np.EVENT_TICK, self.tick)

    def tick(self, notification: bn.BaseNotification, delta: float) -> None:
        self.timer += delta
        self.alpha = self.startAlpha + \
            (self.endAlpha - self.startAlpha) * \
            self.tweenFunc(min(1.0, self.timer / self.duration))
        if self.alpha >= self.endAlpha:
            self.alpha = self.endAlpha
            notification.remove_on(np.EVENT_TICK, self.tick)
        notification.attributes("-alpha", self.alpha)


class GrowDownTransition():
    def __init__(self, duration: float = 1.0, startHeight: int = 0,
                 endHeight: int = 100, tweenFunc: callable = tween.linear):
        self.duration = duration
        self.startHeight = startHeight
        self.endHeight = endHeight
        self.tweenFunc = tweenFunc
        self.timer = 0.0
        self.bound = False

    def bind(self, notification: bn.BaseNotification) -> None:
        if self.bound:
            raise "Cannot bind the same transition to more than one notification"
        notification.on(np.EVENT_BEFORE_OPEN, self.before_open)
        self.bound = True

    def before_open(self, notification: bn.BaseNotification) -> None:
        self.timer = 0.0
        notification.geometry(
            f"{notification.winfo_width()}x{self.startHeight}")
        notification.on(np.EVENT_TICK, self.tick)

    def tick(self, notification: bn.BaseNotification, delta: float) -> None:
        self.timer += delta
        self.height = int(self.startHeight +
                          (self.endHeight - self.startHeight) *
                          self.tweenFunc(min(1.0, self.timer / self.duration)))
        if self.height >= self.endHeight:
            self.height = self.endHeight
            notification.remove_on(np.EVENT_TICK, self.tick)
        notification.geometry(
            f"{notification.winfo_width()}x{self.height}")


class AlphaFadeOutTransition():
    def __init__(self, duration: float = 1.0, startAlpha: float = 1.0,
                 endAlpha: float = 0.0, tweenFunc: callable = tween.linear):
        self.duration = duration
        self.startAlpha = startAlpha
        self.endAlpha = endAlpha
        self.tweenFunc = tweenFunc
        self.timer = 0.0
        self.bound = False

    def bind(self, notification: bn.BaseNotification) -> None:
        if self.bound:
            raise "Cannot bind the same transition to more than one notification"
        notification.destroyOnCloseEvent = False
        notification.on(np.EVENT_CLOSE, self.on_close)
        self.bound = True

    def on_close(self, notification: bn.BaseNotification) -> None:
        self.timer = 0.0
        notification.attributes("-alpha", self.startAlpha)
        notification.on(np.EVENT_TICK, self.tick)

    def tick(self, notification: bn.BaseNotification, delta: float) -> None:
        self.timer += delta
        self.alpha = self.startAlpha + \
            (self.endAlpha - self.startAlpha) * \
            self.tweenFunc(min(1.0, self.timer / self.duration))
        if self.alpha <= self.endAlpha:
            notification.remove_on(np.EVENT_TICK, self.tick)
            notification.destroy()
        else:
            notification.attributes("-alpha", self.alpha)
