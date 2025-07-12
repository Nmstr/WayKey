from evdev import ecodes as e
import socket
import json

SOCKET_PATH = "/tmp/waykeyd.sock"

def _send_command(command: dict) -> dict:
    """
    Send a command to the daemon and get the response
    """
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(SOCKET_PATH)
        client.sendall(json.dumps(command).encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        return json.loads(response)
    finally:
        client.close()

def _convert_code(code: str) -> int or None:
    """
    Convert a key code from string to integer
    """
    for key, value in e.keys.items():
        if isinstance(value, tuple):
            for v in value:
                if v == code:
                    return key
        else:
            if value == code:
                return key
    return None

def press(code: str | int, device_id: str = "default_device") -> dict:
    """
    Press a key
    """
    if not isinstance(code, int):
        code = _convert_code(code)
    if code is None:
        raise ValueError(f"Invalid key code: {code}")
    return _send_command({
        "type": "press",
        "code": code,
        "device_id": device_id
    })

def release(code: str | int, device_id: str = "default_device") -> dict:
    """
    Release a key
    """
    if not isinstance(code, int):
        code = _convert_code(code)
    if code is None:
        raise ValueError(f"Invalid key code: {code}")
    return _send_command({
        "type": "release",
        "code": code,
        "device_id": device_id
    })

def click(code: str | int, device_id: str = "default_device", delay: int = 0) -> dict:
    """
    Click a key
    """
    if not isinstance(code, int):
        code = _convert_code(code)
    if code is None:
        raise ValueError(f"Invalid key code: {code}")
    return _send_command({
        "type": "click",
        "code": code,
        "device_id": device_id,
        "delay": delay
    })

def mouse_move(x: int, y: int, w: int = 0, absolute: bool = False, device_id: str = "default_device") -> dict:
    """
    Move the mouse cursor
    """
    return _send_command({
        "type": "mouse_move",
        "x": x,
        "y": y,
        "w": w,
        "absolute": absolute,
        "device_id": device_id
    })

def get_devices() -> dict:
    """
    Get a list of all devices
    """
    return _send_command({
        "type": "get_devices"
    })

def load_device(device_id: str = "default_device") -> dict:
    """
    Load a device by its ID
    """
    return _send_command({
        "type": "load_device",
        "device_id": device_id
    })

def unload_device(device_id: str = "default_device") -> dict:
    """
    Unload a device by its ID
    """
    return _send_command({
        "type": "unload_device",
        "device_id": device_id
    })
