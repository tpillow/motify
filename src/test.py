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


test = bn.SimpleTextNotificationWithTimeoutBar(
    "Hello, Notification! I have no idea what happens when the text out-grows the screen.",
    backgroundColor=COLOR_BG, textColor=COLOR_BASE, closeOnClick=True,
    hoverBackgroundColor=COLOR_BG_DARKER, hoverTextColor=COLOR_BASE_LIGHER,
    hoverBorderColor=COLOR_HEADER, borderColor=COLOR_SECONDARY, cursor="spider",
    timeoutBarBackgroundColor=COLOR_BG, timeoutBarForegroundColor=COLOR_HEADER,
    timeout=3.0, hAlign=np.HAlignment.RIGHT, vAlign=np.VAlignment.CENTER)

fadeIn = nt.AlphaFadeInTransition()
fadeIn.bind(test)

growDown = nt.GrowDownTransition(
    duration=0.3, endHeight=test.winfo_height())
growDown.bind(test)

fadeOut = nt.AlphaFadeOutTransition(tweenFunc=tween.easeOutBack)
fadeOut.bind(test)

test.show_notification()
