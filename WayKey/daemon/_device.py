from evdev import UInput, AbsInfo, ecodes as e
import json
import os

def get_path_from_id(device_id: str) -> str or None:
    """
    Returns the path to the device file based on the device ID.
    """
    device_dir = os.path.expanduser(os.path.join("~", ".config", "waykey", "devices"))
    if not os.path.exists(device_dir):
        raise FileNotFoundError(f"Device directory {device_dir} does not exist.")
    for filename in os.listdir(device_dir):
        with open(os.path.join(device_dir, filename), 'r') as f:
            device_info = json.loads(f.read())
            if device_info.get("id") == device_id:
                return os.path.join(device_dir, filename)
    return None

def is_id_valid(device_id: str) -> bool:
    """
    Checks if any given device ID is valid.
    """
    if device_id == "default_device":
        return True
    device_dir = os.path.expanduser(os.path.join("~", ".config", "waykey", "devices"))
    if not os.path.exists(device_dir):
        return False
    for filename in os.listdir(device_dir):
        with open(os.path.join(device_dir, filename), 'r') as f:
            device_info = json.loads(f.read())
            if device_info.get("id") == device_id:
                return True
    return False

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
            if isinstance(value, tuple):
                for v in value:
                    if v in self.device_info.get("keys", []) and key not in key_list:
                        key_list.append(key)
            else:
                if value in self.device_info.get("keys", []) and key not in key_list:
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
