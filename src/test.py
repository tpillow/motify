# Imports
import base_notification as bn
import notification_transition as nt
import pytweening as tween

test = bn.BaseNotification()

fadeIn = nt.AlphaFadeInTransition()
fadeIn.bind(test)

fadeOut = nt.AlphaFadeOutTransition(tweenFunc=tween.easeOutBack)
fadeOut.bind(test)

test.show_notification()

print("Done")
