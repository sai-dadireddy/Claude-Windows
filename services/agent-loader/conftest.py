"""
Pytest configuration for agent-loader tests.

This conftest.py ensures pytest can run tests without conflicting
with the package __init__.py that has relative imports.
"""

import sys
import os

# Add the current directory to path so lambda_function can be imported directly
sys.path.insert(0, os.path.dirname(__file__))

# Tell pytest to ignore __init__.py
collect_ignore = ["__init__.py"]
