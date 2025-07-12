from _device import init_device, get_path_from_id, is_id_valid
from evdev import ecodes as e
import socket
import json
import time
import os

SOCKET_PATH = '/tmp/waykeyd.sock'
input_devices = {}

def click(command: dict, device_id: str) -> dict:
    delay = command.get("delay", 0)
    input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 1)
    input_devices[device_id].uinput.syn()
    time.sleep(delay)
    input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 0)
    input_devices[device_id].uinput.syn()
    return {"status": "success", "message": "Click event processed"}

def press(command: dict, device_id: str) -> dict:
    input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 1)
    input_devices[device_id].uinput.syn()
    return {"status": "success", "message": "Press event processed"}

def release(command: dict, device_id: str) -> dict:
    input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 0)
    input_devices[device_id].uinput.syn()
    return {"status": "success", "message": "Release event processed"}

def mouse_move(command: dict, device_id: str) -> dict:
    absolute = command.get("absolute", False)
    x = command.get("x", 0)
    y = command.get("y", 0)
    w = command.get("w", 0)
    if absolute:
        input_devices[device_id].uinput.write(e.EV_ABS, e.ABS_X, x)
        input_devices[device_id].uinput.write(e.EV_ABS, e.ABS_Y, y)
    else:
        input_devices[device_id].uinput.write(e.EV_REL, e.REL_X, x)
        input_devices[device_id].uinput.write(e.EV_REL, e.REL_Y, y)
        input_devices[device_id].uinput.write(e.EV_REL, e.REL_WHEEL, w)
    input_devices[device_id].uinput.syn()
    return {"status": "success", "message": "Mouse event processed"}

def get_devices() -> dict:
    devices = [device.device_info for device_id, device in input_devices.items()]
    return {"status": "success", "devices": devices}

def load_device(command: dict) -> dict:
    new_id = command.get("device_id", None)
    if not new_id:
        return {"status": "error", "message": "Device ID is required"}
    device_path = get_path_from_id(new_id)
    if not device_path:
        return {"status": "error", "message": f"Device with ID {new_id} not found"}
    device_id, device = init_device(device_path)
    input_devices[device_id] = device
    return {"status": "success", "message": f"Device {device_id} loaded"}

def unload_device(command: dict) -> dict:
    device_id = command.get("device_id", None)
    if not is_id_valid(device_id):
        return {"status": "error", "message": f"Invalid device ID: {device_id}"}
    if device_id not in input_devices:
        return {"status": "error", "message": f"Device {device_id} not found"}
    del input_devices[device_id]
    return {"status": "success", "message": f"Device {device_id} unloaded"}

def process_command(command: dict) -> dict:
    command_type = command.get("type")
    device_id = command.get("device_id", "default_device")
    if not is_id_valid(device_id):
        return {"status": "error", "message": f"Invalid device ID: {device_id}"}

    if command_type == "click":
        return click(command, device_id)

    elif command_type == "press":
        return press(command, device_id)

    elif command_type == "release":
        return release(command, device_id)

    elif command_type == "mouse_move":
        return mouse_move(command, device_id)

    elif command_type == "get_devices":
        return get_devices()

    elif command_type == "load_device":
        return load_device(command)

    elif command_type == "unload_device":
        return unload_device(command)

    return {"status": "error", "message": "Unknown command"}

def main() -> None:
    # Remove socket if it already exists
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    # Initialize default input device
    device_id, device = init_device()
    input_devices[device_id] = device
    print(f"Initialized device: {device_id}")

    # Create server socket
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)
    print(f"Daemon listening on {SOCKET_PATH}")

    try:
        while True:
            conn, addr = server.accept()
            try:
                data = conn.recv(4096).decode('utf-8')
                if not data:
                    continue
                
                command = json.loads(data)
                print(f"Received command: {command}")
                
                response = process_command(command)
                conn.sendall(json.dumps(response).encode('utf-8'))
            finally:
                conn.close()
    finally:
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.unlink(SOCKET_PATH)

if __name__ == "__main__":
    main()
