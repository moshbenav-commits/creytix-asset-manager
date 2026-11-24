#!/usr/bin/env python3
"""
asset_manager.py — BACKWARD-COMPAT WRAPPER.

The audio asset manager is now unified: all types (audio, video, image, 3d,
document) live in unified_registry.py with a single registry.json.

This wrapper forwards every call unchanged, e.g.:
    asset_manager.py register <file> --voice ID --prompt "..."
        -> unified_registry.py register <file> --voice ID --prompt "..."

Original implementation preserved at asset_manager.py.orig.
"""

import subprocess
import sys
from pathlib import Path

UNIFIED = Path(__file__).parent / "unified_registry.py"

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, str(UNIFIED)] + sys.argv[1:]))
