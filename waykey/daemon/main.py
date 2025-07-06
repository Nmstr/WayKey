from _device import init_device
from evdev import ecodes as e
import socket
import json
import time
import os

SOCKET_PATH = '/tmp/waykeyd.sock'
ui = init_device()

def main():
    # Remove socket if it already exists
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)
    
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
    if command_type == "click":
        delay = command.get("delay", 0)
        ui.write(e.EV_KEY, command["code"], 1)
        ui.syn()
        time.sleep(delay)
        ui.write(e.EV_KEY, command["code"], 0)
        ui.syn()
        return {"status": "success", "message": "Click event processed"}

    elif command_type == "press":
        ui.write(e.EV_KEY, command["code"], 1)
        ui.syn()
        return {"status": "success", "message": "Press event processed"}

    elif command_type == "release":
        ui.write(e.EV_KEY, command["code"], 0)
        ui.syn()
        return {"status": "success", "message": "Release event processed"}

    elif command_type == "mouse_move":
        absolute = command.get("absolute", False)
        x = command.get("x", 0)
        y = command.get("y", 0)
        w = command.get("w", 0)
        if absolute:
            ui.write(e.EV_ABS, e.ABS_X, x)
            ui.write(e.EV_ABS, e.ABS_Y, y)
        else:
            ui.write(e.EV_REL, e.REL_X, x)
            ui.write(e.EV_REL, e.REL_Y, y)
            ui.write(e.EV_REL, e.REL_WHEEL, w)
        ui.syn()
        return {"status": "success", "message": "Mouse event processed"}

    return {"status": "error", "message": "Unknown command"}

if __name__ == "__main__":
    main()
