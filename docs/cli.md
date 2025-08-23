# Cli

The WayKey CLI consists of 5 main components (`press`, `release`, `click`, `mouse_move` and `device`). Each component will be described in detail below.

# Press

Press takes one key code as an argument and presses the corresponding key. The key will not be released automatically (refer to `release` to release the key again).
Optionally, a device can be specified with the `-d` flag.

Examples:
```bash
waykey press KEY_A
waykey press KEY_A -d ~/path/to/device.json
```

# Release

Release takes one key code as an argument and releases the corresponding key. The key must have been pressed before for this to have an effect (refer to `press` to press the key).
Optionally, a device can be specified with the `-d` flag.

Examples:
```bash
waykey release KEY_A
waykey release KEY_A -d ~/path/to/device.json
```

# Click

Click takes one key code as an argument and clicks the corresponding key by both pressing and automatically releasing it after a short delay.
Optionally, a device can be specified with the `-d` flag.
It also has an optional `--delay` flag to specify the delay between pressing and releasing the key in seconds (default is 0s).

Examples:
```bash
waykey click KEY_A
waykey click KEY_A -d ~/path/to/device.json
waykey click KEY_A --delay 0.5
waykey click KEY_A -d ~/path/to/device.json --delay 0.5
```

# Mouse Move

Mouse Move takes two arguments, `x` and `y`, which specify the position to move the mouse to (absolute movement) or the distance to move the mouse by (relative movement).
By default, the movement is relative. Absolute movement can be enabled with the `--absolute` flag.
The mouse wheel can be scrolled with the `-w` flag, which takes an integer argument. It is not possible to combine wheel movement with absolute mouse movement.
Optionally, a device can be specified with the `-d` flag.

Examples:
```bash
waykey mouse_move 100 100
waykey mouse_move 100 100 -d ~/path/to/device.json
waykey mouse_move 100 100 --absolute
waykey mouse_move 100 100 --absolute -d ~/path/to/device.json
waykey mouse_move 0 0 -w 100
waykey mouse_move 0 0 -w 100 -d ~/path/to/device.json
waykey mouse_move 200 200 -w -100
```

# Device

The device component is used to manage virtual input devices. It has 3 subcomponents (`list`, `load` and `unload`). Each subcomponent will be described in detail below.

## List

List lists all currently loaded virtual input devices. The list shows the device ID and Name.

Examples:
```bash
waykey device list
```

## Load

Load takes the ID of a device as an argument and attempts to load that device.

Examples:
```bash
waykey device load my_device_id
```

## Unload

Unload takes the ID of a device as an argument and attempts to unload that device.

Examples:
```bash
waykey device unload my_device_id
```
