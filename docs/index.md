# WayKey

![Image](./assets/WayKey.svg)

WayKey is a wayland automation tool.

# Installation

## Manual (Recommended)

1. Clone the repository:
```bash
git clone git@github.com:Nmstr/WayKey.git
cd WayKey
```

2. Install dependencies:
```bash
uv sync
```

3. Create links:
```bash
sudo ln -s $(pwd)/WayKey/cli/run.sh /usr/bin/waykey
sudo ln -s $(pwd)/WayKey/daemon/run.sh /usr/bin/waykeyd
```

# Basic Usage

Start the daemon:
```bash
waykeyd
# or
sudo waykeyd
```

Click a Key:
```bash
waykey click KEY_A
# or
sudo waykey click KEY_A
```

Whether to use `sudo` or not depends on your system configuration.
