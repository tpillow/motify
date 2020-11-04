# So we can access the notification stuff
import notifications as bn
import transitions as nt
import components as comps
import pytweening as tween

# Imports

COLOR_BG: str = "#34344A"
COLOR_BG_DARKER: str = "#232339"
COLOR_HEADER: str = "#F0F757"
COLOR_SECONDARY: str = "#F24C00"
COLOR_BASE: str = "#F9E0D9"
COLOR_BASE_LIGHER: str = "#FAF9EA"


def ok_callback():
    print("OK_PRESSED")


def begin_close(notification: bn.BaseNotification):
    notification.emit_notification_close()


test = bn.BaseNotification(borderColor=COLOR_SECONDARY, cursor="spider",
                           timeout=3.0, hAlign=bn.HAlignment.RIGHT, vAlign=bn.VAlignment.CENTER)

test.addComponent(comps.TextComponent("Hello, Notification! I have no idea what happens when the text out-grows the screen.",
                                      backgroundColor=COLOR_BG, textColor=COLOR_BASE, justify="left"))

test.addComponent(comps.TimeoutProgressBarComponent(
    timeoutBarBackgroundColor=COLOR_BG, timeoutBarForegroundColor=COLOR_HEADER))

test.addComponent(comps.ButtonComponent(
    [("OK", ok_callback), ("CANCEL", ok_callback)]))

test.on(bn.EVENT_CLICKED, begin_close)


test.addComponent(nt.AlphaFadeInTransition())
test.addComponent(nt.GrowDownTransition(
    duration=0.3, endHeight=test.winfo_height()))
test.addComponent(nt.AlphaFadeOutTransition())
test.addComponent(nt.ShrinkUpTransition(
    duration=0.3, startHeight=test.winfo_height()))

test.show_notification()
