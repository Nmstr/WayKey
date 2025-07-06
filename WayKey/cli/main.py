from evdev import ecodes as e
import socket
import json
import time

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

if __name__ == "__main__":
    press_key(e.KEY_LEFTSHIFT)
    click_key(e.KEY_H)
    release_key(e.KEY_LEFTSHIFT)
    click_key(e.KEY_E)
    click_key(e.KEY_L)
    click_key(e.KEY_L)
    click_key(e.KEY_O)
    click_key(e.KEY_SPACE)
    press_key(e.KEY_LEFTSHIFT)
    click_key(e.KEY_W)
    release_key(e.KEY_LEFTSHIFT)
    click_key(e.KEY_O)
    click_key(e.KEY_R)
    click_key(e.KEY_L)
    click_key(e.KEY_D)
    press_key(e.KEY_LEFTSHIFT)
    click_key(e.KEY_1)
    release_key(e.KEY_LEFTSHIFT)
    time.sleep(0.1)

    mouse_move(500, 500, absolute=True)
    for i in range(100):
        mouse_move(10, 0)
        time.sleep(0.025)
    mouse_move(0, 0, w=100)
