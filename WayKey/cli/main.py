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

def press_key(code) -> dict:
    """
    Press a key
    """
    return send_command({
        "type": "press",
        "code": code
    })

def release_key(code) -> dict:
    """
    Release a key
    """
    return send_command({
        "type": "release",
        "code": code
    })

def click_key(code) -> dict:
    """
    Click a key
    """
    return send_command({
        "type": "click",
        "code": code
    })

def mouse_move(x: int, y: int, w: int = 0, absolute: bool = False) -> dict:
    """
    Move the mouse cursor
    """
    return send_command({
        "type": "mouse_move",
        "x": x,
        "y": y,
        "w": w,
        "absolute": absolute
    })

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WayKey CLI')
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")
    
    # Key commands (press, release, click)
    for cmd in ["press", "release", "click"]:
        key_parser = subparsers.add_parser(cmd, help=f"{cmd.capitalize()} a key")
        key_parser.add_argument("key", type=str, help="Key code to use")
    # Mouse move command
    mouse_parser = subparsers.add_parser("mouse_move", help="Move the mouse cursor")
    mouse_parser.add_argument("x", type=int, help="X coordinate")
    mouse_parser.add_argument("y", type=int, help="Y coordinate")
    mouse_parser.add_argument("-w", type=int, default=0, help="Wheel movement (Only for relative movement)")
    mouse_parser.add_argument("-a", "--absolute", action='store_true', help="Use absolute coordinates")

    device_parser = subparsers.add_parser("device", help="Manage devices")
    device_subparsers = device_parser.add_subparsers(dest="device_command", required=True, help="Device command to execute")

    device_subparsers.add_parser("list", help="List available devices")
    load_parser = device_subparsers.add_parser("load", help="Load a device by ID")
    load_parser.add_argument("id", type=str, help="ID of the device to load")

    args = parser.parse_args()

    if args.command in ["press", "release", "click"]:
        try:
            key_code = getattr(e, args.key)
            if args.command == "press":
                press_key(key_code)
            elif args.command == "release":
                release_key(key_code)
            elif args.command == "click":
                click_key(key_code)
        except AttributeError:
            print(f"Error: Invalid key code '{args.key}'.")
            exit(1)
    elif args.command == "mouse_move":
        if args.absolute and args.w:
            print("Error: Wheel movement can not be used with absolute movement.")
            exit(1)
        mouse_move(args.x, args.y, args.w, args.absolute)
    elif args.command == "device":
        if args.device_command == "list":
            list_devices()
        elif args.device_command == "load":
            pass

