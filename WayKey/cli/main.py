from evdev import ecodes as e
import argparse
import socket
import json

SOCKET_PATH = "/tmp/waykeyd.sock"

def send_command(command: dict) -> dict:
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

def press_key(code: str, device_id: str) -> None:
    """
    Press a key
    """
    response = send_command({
        "type": "press",
        "code": code,
        "device_id": device_id
    })
    if response.get("status") == "success":
        print(f"Key {code} pressed successfully.")
    else:
        print(f"Failed to press key {code}: {response.get('message', 'Unknown error')}")

def release_key(code: str, device_id: str) -> None:
    """
    Release a key
    """
    response = send_command({
        "type": "release",
        "code": code,
        "device_id": device_id
    })
    if response.get("status") == "success":
        print(f"Key {code} released successfully.")
    else:
        print(f"Failed to release key {code}: {response.get('message', 'Unknown error')}")

def click_key(code: str, device_id: str, delay: int = 0) -> None:
    """
    Click a key
    """
    response = send_command({
        "type": "click",
        "code": code,
        "device_id": device_id,
        "delay": delay
    })
    if response.get("status") == "success":
        print(f"Key {code} clicked successfully.")
    else:
        print(f"Failed to click key {code}: {response.get('message', 'Unknown error')}")

def mouse_move(x: int, y: int, w: int = 0, absolute: bool = False, device_id: str = "default_device") -> None:
    """
    Move the mouse cursor
    """
    response = send_command({
        "type": "mouse_move",
        "x": x,
        "y": y,
        "w": w,
        "absolute": absolute,
        "device_id": device_id
    })
    if response.get("status") == "success":
        print(f"Mouse moved to ({x}, {y}) with wheel movement {w} {'(absolute)' if absolute else '(relative)'} successfully.")
    else:
        print(f"Failed to move mouse: {response.get('message', 'Unknown error')}")

def list_devices() -> None:
    """
    List available devices
    """
    response = send_command({
        "type": "get_devices"
    })
    devices = response.get("devices", [])
    if not devices:
        print("No devices found.")
        return
    id_width = max(len(devices.get("id", "")) for devices in devices)
    name_width = max(len(devices.get("name", "")) for devices in devices)
    print("Available devices:")
    print(f"{'ID':<{id_width}}\t{'Name':<{name_width}}")
    for device_info in response.get("devices", []):
        print(f"{device_info.get('id', ''):<{id_width}}\t{device_info.get('name', ''):<{name_width}}")

def load_device(device_id: str) -> None:
    """
    Load a device by ID
    """
    response = send_command({
        "type": "load_device",
        "id": device_id
    })
    if response.get("status") == "success":
        print(f"Device {device_id} loaded successfully.")
    else:
        print(f"Failed to load device {device_id}: {response.get('message', 'Unknown error')}")

def unload_device(device_id: str) -> None:
    """
    Unload a device by ID
    """
    response = send_command({
        "type": "unload_device",
        "id": device_id
    })
    if response.get("status") == "success":
        print(f"Device {device_id} unloaded successfully.")
    else:
        print(f"Failed to unload device {device_id}: {response.get('message', 'Unknown error')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WayKey CLI')
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")
    
    # Key commands (press, release, click)
    for cmd in ["press", "release", "click"]:
        key_parser = subparsers.add_parser(cmd, help=f"{cmd.capitalize()} a key")
        key_parser.add_argument("key", type=str, help="Key code to use")
        key_parser.add_argument("-d", type=str, default="default_device", help="ID of the device to use (default: 'default_device')")
        if cmd == "click":
            key_parser.add_argument("--delay", type=float, default=0, help="Delay between the press and release (in seconds)")
    # Mouse move command
    mouse_parser = subparsers.add_parser("mouse_move", help="Move the mouse cursor")
    mouse_parser.add_argument("x", type=int, help="X coordinate")
    mouse_parser.add_argument("y", type=int, help="Y coordinate")
    mouse_parser.add_argument("-w", type=int, default=0, help="Wheel movement (Only for relative movement)")
    mouse_parser.add_argument("-a", "--absolute", action='store_true', help="Use absolute coordinates")
    mouse_parser.add_argument("-d", type=str, default="default_device", help="ID of the device to use (default: 'default_device')")

    device_parser = subparsers.add_parser("device", help="Manage devices")
    device_subparsers = device_parser.add_subparsers(dest="device_command", required=True, help="Device command to execute")

    device_subparsers.add_parser("list", help="List available devices")
    load_parser = device_subparsers.add_parser("load", help="Load a device by ID")
    load_parser.add_argument("id", type=str, help="ID of the device to load")
    unload_parser = device_subparsers.add_parser("unload", help="Unload a device by ID")
    unload_parser.add_argument("id", type=str, help="ID of the device to unload")

    args = parser.parse_args()

    if args.command in ["press", "release", "click"]:
        try:
            key_code = getattr(e, args.key)
            device_id = args.d
            if args.command == "press":
                press_key(key_code, device_id)
            elif args.command == "release":
                release_key(key_code, device_id)
            elif args.command == "click":
                click_key(key_code, device_id, args.delay)
        except AttributeError:
            print(f"Error: Invalid key code '{args.key}'.")
            exit(1)
    elif args.command == "mouse_move":
        device_id = args.d
        if args.absolute and args.w:
            print("Error: Wheel movement can not be used with absolute movement.")
            exit(1)
        mouse_move(args.x, args.y, args.w, args.absolute, device_id)
    elif args.command == "device":
        if args.device_command == "list":
            list_devices()
        elif args.device_command == "load":
            load_device(args.id)
        elif args.device_command == "unload":
            unload_device(args.id)
