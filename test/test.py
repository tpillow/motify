# Imports
from motify import *
import time

# Colors
COLOR_BG: str = "#34344A"
COLOR_BG_DARKER: str = "#232339"
COLOR_TEXT: str = "#F9E0D9"
COLOR_SECONDARY: str = "#F24C00"


def show_blank_base_notification():
    notif = BaseNotification(timeout=0.5)
    notif.show_notification()


def show_blank_base_notification_with_alpha_fades():
    notif = BaseNotification(timeout=1.5)
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
    notif.show_notification()


def show_blank_base_notification_with_grow_shrink():
    notif = BaseNotification(timeout=1.5)
    notif.add_component(GrowDownTransition())
    notif.add_component(ShrinkUpTransition())
    notif.show_notification()


def show_blank_base_notification_with_alpha_fades_grow_shrink():
    notif = BaseNotification(timeout=1.5)
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
    notif.add_component(GrowDownTransition())
    notif.add_component(ShrinkUpTransition())
    notif.show_notification()


def show_text_notification():
    notif = TextNotification(
        "This here be some text. Maybe two lines worth.", timeout=1.0)
    notif.show_notification()


def show_image_large_size_center_notification():
    notif = ImageNotification("./test/buddah.gif", width=480, height=400,
                              hAlign=HAlignment.CENTER, vAlign=VAlignment.CENTER, timeout=1.0)
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
    notif.show_notification()


def show_image_large_size_center_notification_print_click():
    notif = ImageNotification("./test/buddah.gif", width=480, height=400,
                              hAlign=HAlignment.CENTER, vAlign=VAlignment.CENTER, timeout=1.0)
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
    notif.on(EVENT_CLICKED, lambda notification: print("Clicked"))
    notif.show_notification()


def show_text_notification_alpha_fades_grow_shring():
    notif = TextNotification(
        "This here be some text. Maybe two lines worth.", timeout=1.0)
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
    notif.add_component(GrowDownTransition())
    notif.add_component(ShrinkUpTransition())
    notif.show_notification()


def show_text_notification_timeout_bar():
    notif = TextNotification(
        "This here be some text. Maybe two lines worth.", timeout=1.5)
    bar = TimeoutProgressBarComponent()
    notif.add_component(bar)
    bar.canvas.pack(fill=tk.X)
    notif.show_notification()


def show_text_notification_context_menu_timeout_bar():
    notif = TextNotification(
        "This here be some text. Maybe two lines worth.", timeout=2.0)
    notif.add_component(ContextMenuComponent(
        [("Option A", lambda: print("A")), ("Option B", lambda: print("B"))]))
    bar = TimeoutProgressBarComponent()
    notif.add_component(bar)
    bar.canvas.pack(fill=tk.X)
    notif.show_notification()


def show_text_notification_timeout_bar_stop_hover():
    notif = TextNotification(
        "This here be some text. Maybe two lines worth.", timeout=1.5)
    bar = TimeoutProgressBarComponent()
    notif.add_component(bar)
    bar.canvas.pack(fill=tk.X)
    notif.add_component(StopTimeoutOnHoverComponent())
    notif.show_notification()


def show_text_notification_timeout_bar_stop_hover_alpha_fade():
    notif = TextNotification(
        "This here be some text. Maybe two lines worth.", timeout=1.5)
    bar = TimeoutProgressBarComponent()
    notif.add_component(bar)
    bar.canvas.pack(fill=tk.X)
    notif.add_component(StopTimeoutOnHoverComponent())
    notif.add_component(AlphaFadeInTransition())
    notif.add_component(AlphaFadeOutTransition())
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
    show_text_notification,
    show_image_large_size_center_notification,
    show_text_notification_alpha_fades_grow_shring,
    show_text_notification_timeout_bar,
    show_text_notification_context_menu_timeout_bar,
    show_text_notification_timeout_bar_stop_hover,
    show_text_notification_timeout_bar_stop_hover_alpha_fade,
    show_image_large_size_center_notification_print_click,
])
