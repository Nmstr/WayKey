# Library

The WayKey library provides a python interface to interact with the WayKey daemon. It mirrors the functionality of the CLI, but is much more performant.

# Building

```bash
uv build
```

# Usage

## Importing

```python
import WayKey as wk
```

## Press

Presses a key.

Arguments:
- `code` (str | int): The key code to press (e.g. "KEY_A" or 42).
- `device_id` (str, optional): ID of the device. If not provided, the default device will be used.

```python
wk.press("KEY_A")  # The integer key code can also be used directly
wk.press("KEY_A", device_id="my_device_id")
```

## Release

Releases a key.

Arguments:
- `code` (str | int): The key code to release (e.g. "KEY_A" or 42).
- `device_id` (str, optional): ID of the device. If not provided, the default device will be used.

```python
wk.release("KEY_A")  # The integer key code can also be used directly
wk.release("KEY_A", device_id="my_device_id")
```

## Click

Clicks a key by pressing and releasing it.

Arguments:
- `code` (str | int): The key code to click (e.g. "KEY_A" or 42).
- `device_id` (str, optional): ID of the device. If not provided, the default device will be used.
- `delay` (float, optional): Delay between pressing and releasing the key in seconds. Default is 0.

```python
wk.click("KEY_A")  # The integer key code can also be used directly
wk.click("KEY_A", device_id="my_device_id")
wk.click("KEY_A", delay=0.5)
wk.click("KEY_A", device_id="my_device_id", delay=0.5)
```

## Mouse Move

Moves the mouse either absolutely or relatively, and can also scroll the mouse wheel.

Arguments:
- `x` (int): The x position to move the mouse to (absolute movement) or the distance to move the mouse by (relative movement).
- `y` (int): The y position to move the mouse to (absolute movement) or the distance to move the mouse by (relative movement).
- `w` (int, optional): Amount to scroll the mouse wheel. Default is 0 (no scrolling). This can not be used with absolute movement.
- `absolute` (bool, optional): Whether to use absolute movement. Default is False (relative movement).
- `device_id` (str, optional): ID of the device. If not provided, the default device will be used.

```python
wk.mouse_move(100, 100)
wk.mouse_move(100, 100, device_id="my_device_id")
wk.mouse_move(100, 100, absolute=True)
wk.mouse_move(100, 100, absolute=True, device_id="my_device_id")
wk.mouse_move(0, 0, w=100)
wk.mouse_move(0, 0, w=100, device_id="my_device_id")
wk.mouse_move(200, 200, w=-100)
```

## Get Devices

Returns a dictionary of all available devices.

```python
devices = wk.get_devices()
print(devices)
```

## Load Device

Loads a device by its ID.

Arguments:
- `device_id` (str): ID of the device to load.

```python
wk.load_device("my_device_id")
```

## Unload Device

Unloads a device by its ID.

Arguments:
- `device_id` (str): ID of the device to unload.

```python
wk.unload_device("my_device_id")
```
