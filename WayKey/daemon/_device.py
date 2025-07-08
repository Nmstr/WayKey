from evdev import UInput, AbsInfo, ecodes as e
import json
import os

def init_device(device_path: str = None) -> tuple:
    """
    Initializes an InputDevice
    """
    if device_path is None:
        device_path = os.path.expanduser(os.path.join(os.getcwd(), "WayKey", "daemon", "default_device.json"))
    if not os.path.exists(device_path):
        raise FileNotFoundError(f"Device {device_path} not found.")
    with open(device_path, 'r') as f:
        device_info = json.loads(f.read())
    if not device_info.get("id", None):
        raise ValueError(f"Device {device_path} does not have a valid ID.")

    device = InputDevice(device_path=device_path)
    return device_info["id"], device

class InputDevice:
    def __init__(self, device_path: str):
        """
        Initializes the virtual input device with the necessary capabilities.
        Returns a UInput instance.
        """
        with open(device_path, 'r') as f:
            self.device_info = json.loads(f.read())

        key_list = []
        for key, value in e.keys.items():
            if value in self.device_info.get("keys", []):
                key_list.append(key)

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

        self.uinput = UInput(cap, self.device_info.get("name", "Unnamed WayKey Device"),)
