# Imports
from motify import *
import time

# Colors
COLOR_BG: str = "#34344A"
COLOR_BG_DARKER: str = "#232339"
COLOR_TEXT: str = "#F9E0D9"
COLOR_SECONDARY: str = "#F24C00"


def callback_ok():
    print("Callback OK was triggered")


def callback_cancel():
    print("Callback CANCEL was triggered")


def trigger_notification_close_callback(notification: BaseNotification):
    # Emit the notification close event right now
    notification.emit_notification_close()


def show_blank_base_notification():
    notif = BaseNotification(timeout=0.5, closeOnTimeout=True)
    notif.show_notification()


def show_blank_base_notification_with_alpha_fades():
    notif = BaseNotification(timeout=1.5, closeOnTimeout=True)
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
    notif.show_notification()


def show_blank_base_notification_with_grow_shrink():
    notif = BaseNotification(timeout=1.5, closeOnTimeout=True)
    notif.add_component(GrowDownTransition())
    notif.add_component(ShrinkUpTransition())
    notif.show_notification()


def show_blank_base_notification_with_alpha_fades_grow_shrink():
    notif = BaseNotification(timeout=1.5, closeOnTimeout=True)
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
    notif.add_component(GrowDownTransition())
    notif.add_component(ShrinkUpTransition())
    notif.show_notification()


def run_tests(testFuncs: list[callable]):
    for testFunc in testFuncs:
        print(f"Running {getattr(testFunc, '__name__', 'UNDEFINED_NAME')}")
        testFunc()
        time.sleep(0.4)
    print("Done running tests")


# Run all the tests back-to-back (each blocks)
run_tests([
    show_blank_base_notification,
    show_blank_base_notification_with_alpha_fades,
    show_blank_base_notification_with_grow_shrink,
    show_blank_base_notification_with_alpha_fades_grow_shrink,
])
