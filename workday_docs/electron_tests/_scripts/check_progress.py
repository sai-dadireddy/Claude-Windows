#!/usr/bin/env python3
"""Monitor HCM test generation progress"""

import os
import time
from pathlib import Path

OUTPUT_DIR = "HCM"
TOTAL = 439

while True:
    files = list(Path(OUTPUT_DIR).glob("*.txt"))
    count = len(files)

    progress = (count / TOTAL) * 100
    print(f"\rProgress: {count}/{TOTAL} ({progress:.1f}%)    ", end="", flush=True)

    if count >= TOTAL:
        print("\n✓ Complete!")
        break

    time.sleep(5)
