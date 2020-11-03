# Imports
import base_notification as bn
import notification_transition as nt
import notification_properties as np
import pytweening as tween

test = bn.BaseNotification()

fadeIn = nt.AlphaFadeInTransition()
fadeIn.bind(test)

# fadeOut = nt.AlphaFadeOutTransition(tweenFunc=tween.easeOutBack)
# fadeOut.bind(test)

# growDown = nt.GrowDownTransition(
#     duration=0.5, tweenFunc=tween.linear, endHeight=test.winfo_height())
# growDown.bind(test)

test.show_notification()
