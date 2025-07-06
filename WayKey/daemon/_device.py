from evdev import UInput, AbsInfo, ecodes as e

def init_device() -> UInput:
    """
    Initializes the virtual input device with the necessary capabilities.
    Returns a UInput instance.
    """
    key_list = [
        e.KEY_RIGHTCTRL, e.KEY_LEFTCTRL, e.KEY_RIGHTSHIFT, e.KEY_LEFTSHIFT,
        e.KEY_RIGHTMETA, e.KEY_LEFTMETA, e.KEY_RIGHTALT, e.KEY_LEFTALT,
        e.KEY_SPACE, e.KEY_ENTER, e.BTN_MOUSE, e.KEY_TAB,
        e.KEY_0, e.KEY_1, e.KEY_2, e.KEY_3, e.KEY_4, e.KEY_5, e.KEY_6, e.KEY_7, e.KEY_8, e.KEY_9,
        e.KEY_A, e.KEY_B, e.KEY_C, e.KEY_D, e.KEY_E, e.KEY_F, e.KEY_G, e.KEY_H, e.KEY_I, e.KEY_J,
        e.KEY_K, e.KEY_L, e.KEY_M, e.KEY_N, e.KEY_O, e.KEY_P, e.KEY_Q, e.KEY_R, e.KEY_S, e.KEY_T,
        e.KEY_U, e.KEY_V, e.KEY_W, e.KEY_X, e.KEY_Y, e.KEY_Z,
        e.KEY_F1, e.KEY_F2, e.KEY_F3, e.KEY_F4, e.KEY_F5, e.KEY_F6, e.KEY_F7, e.KEY_F8, e.KEY_F9,
        e.KEY_F10, e.KEY_F11, e.KEY_F12, e.KEY_F13, e.KEY_F14, e.KEY_F15, e.KEY_F16, e.KEY_F17,
        e.KEY_F18, e.KEY_F19, e.KEY_F20, e.KEY_F21, e.KEY_F22, e.KEY_F23, e.KEY_F24,
        e.BTN_LEFT, e.BTN_RIGHT, e.BTN_MIDDLE,
        e.KEY_LEFT, e.KEY_UP, e.KEY_RIGHT, e.KEY_DOWN,
        e.KEY_BACKSPACE, e.KEY_DELETE, e.KEY_HOME, e.KEY_END, e.KEY_PAGEUP, e.KEY_PAGEDOWN,
        e.KEY_INSERT, e.KEY_ESC, e.KEY_PAUSE, e.KEY_PRINT, e.KEY_NUMLOCK, e.KEY_CAPSLOCK,
        e.KEY_SCROLLLOCK, e.BTN_TOUCH
    ]

    cap = {
        e.EV_KEY : key_list,
        e.EV_REL : [e.REL_X, e.REL_Y, e.REL_WHEEL],
        e.EV_ABS : [
            (e.ABS_X, AbsInfo(value=0, min=0, max=1920,
                              fuzz=0, flat=0, resolution=0)),
            (e.ABS_Y, AbsInfo(value=0, min=0, max=1080,
                              fuzz=0, flat=0, resolution=0))
        ]
    }

    ui = UInput(cap, name="WayKey virtual input device")
    return ui
