# So we can access the notification stuff
import notifications as bn
import notification_transition as nt
import notification_properties as np
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


test = bn.BaseNotification(borderColor=COLOR_SECONDARY, cursor="spider",
                           timeout=3.0, hAlign=np.HAlignment.RIGHT, vAlign=np.VAlignment.CENTER)

test.addComponent(bn.TextComponent("Hello, Notification! I have no idea what happens when the text out-grows the screen.",
                                   backgroundColor=COLOR_BG, textColor=COLOR_BASE, justify="left"))

test.addComponent(bn.TimeoutProgressBarComponent(
    timeoutBarBackgroundColor=COLOR_BG, timeoutBarForegroundColor=COLOR_HEADER))

test.addComponent(bn.ButtonComponent("OK", ok_callback))


test.addComponent(nt.AlphaFadeInTransition())
test.addComponent(nt.GrowDownTransition(
    duration=0.3, endHeight=test.winfo_height()))
test.addComponent(nt.AlphaFadeOutTransition(tweenFunc=tween.easeOutBack))

test.show_notification()
