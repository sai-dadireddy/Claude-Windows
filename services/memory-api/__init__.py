"""
Memory API Client for Sherpa v4.1
"""

try:
    from .client import MemoryAPIClient, create_client
except ImportError:
    from client import MemoryAPIClient, create_client  # type: ignore[import-not-found]

__version__ = "4.1.0"
__all__ = ["MemoryAPIClient", "create_client"]
