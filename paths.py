import os
import sys

# PyInstaller's onefile mode only extracts real data files (images, etc.) to
# disk under sys._MEIPASS; pure-python packages like `gamescreen/` or
# `gameobjects/` are frozen into the bundle and never exist as real
# directories there. Building asset paths as os.path.dirname(__file__)/../assets
# breaks in that case because the OS can't traverse into a subpackage
# directory that was never extracted. Every asset path must be anchored to
# this single base directory instead.
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
