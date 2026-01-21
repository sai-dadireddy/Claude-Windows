"""
Pytest configuration for agent-loader tests.

Adds the parent directory to sys.path so lambda_function can be imported.
"""

import sys
import os

# Add parent directory (where lambda_function.py is) to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
