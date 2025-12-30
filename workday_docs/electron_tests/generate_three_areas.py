#!/usr/bin/env python3
# Workday Electron Test Generator for Three Areas

import json
import os
import sys
import re
import subprocess
from pathlib import Path

def extract_task_name(task_step):
    if not task_step or str(task_step) == "nan":
        return ""
    task = str(task_step).strip()
    if "Search bar:" in task:
        match = re.search(r"["']([^"']+ )["']" task)
        if match:
            return match.group(1)
    lines = task.split("
")
    if lines:
        first_line = lines[0].strip()
        first_line = re.sub(r"^-\s*", "", first_line)
        first_line = re.sub(r"^Go to\s+", "", first_line, flags=re.IGNORECASE)
        return first_line[:100]
    return task[:100]

print("Test generator ready")
