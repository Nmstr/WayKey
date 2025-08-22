# The next 3 lines are only required if WayKey is not installed as a package.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import WayKey as wk
import time

wk.mouse_move(100, 300, absolute=True)
for i in range(3, 7):
    wk.mouse_move(100, i * 100, absolute=True)
    for j in range(10):
        wk.mouse_move(100, 0)
        time.sleep(0.05)
