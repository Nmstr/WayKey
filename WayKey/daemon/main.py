from _device import init_device, get_path_from_id, is_id_valid
from evdev import ecodes as e
import socket
import json
import time
import os

SOCKET_PATH = '/tmp/waykeyd.sock'
input_devices = {}

def main():
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

def process_command(command):
    command_type = command.get("type")
    device_id = command.get("device_id", "default_device")
    if not is_id_valid(device_id):
        return {"status": "error", "message": f"Invalid device ID: {device_id}"}

    if command_type == "click":
        delay = command.get("delay", 0)
        input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 1)
        input_devices[device_id].uinput.syn()
        time.sleep(delay)
        input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 0)
        input_devices[device_id].uinput.syn()
        return {"status": "success", "message": "Click event processed"}

    elif command_type == "press":
        input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 1)
        input_devices[device_id].uinput.syn()
        return {"status": "success", "message": "Press event processed"}

    elif command_type == "release":
        input_devices[device_id].uinput.write(e.EV_KEY, command["code"], 0)
        input_devices[device_id].uinput.syn()
        return {"status": "success", "message": "Release event processed"}

    elif command_type == "mouse_move":
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

    elif command_type == "get_devices":
        devices = [device.device_info for device_id, device in input_devices.items()]
        return {"status": "success", "devices": devices}

    elif command_type == "load_device":
        id = command.get("id", None)
        if not id:
            return {"status": "error", "message": "Device ID is required"}
        device_path = get_path_from_id(id)
        if not device_path:
            return {"status": "error", "message": f"Device with ID {id} not found"}
        device_id, device = init_device(device_path)
        input_devices[device_id] = device
        return {"status": "success", "message": f"Device {device_id} loaded"}

    return {"status": "error", "message": "Unknown command"}

if __name__ == "__main__":
    main()
