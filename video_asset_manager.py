#!/usr/bin/env python3
"""
video_asset_manager.py — BACKWARD-COMPAT WRAPPER.

The video asset manager is now unified: all types (audio, video, image, 3d,
document) live in unified_registry.py with a single registry.json.

This wrapper forwards every call with --type video injected for `register`
(the unified registry also auto-detects video from extension):
    video_asset_manager.py register <file> --resolution 1920x1080 --fps 30
        -> unified_registry.py register <file> --type video --resolution 1920x1080 --fps 30

Original implementation preserved at video_asset_manager.py.orig.
"""

import subprocess
import sys
from pathlib import Path

UNIFIED = Path(__file__).parent / "unified_registry.py"

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "register" and "--type" not in args:
        args = ["register", "--type", "video"] + args[1:]
    sys.exit(subprocess.call([sys.executable, str(UNIFIED)] + args))
