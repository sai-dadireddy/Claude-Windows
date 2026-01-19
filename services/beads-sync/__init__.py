"""Beads Sync Client for Sherpa v4.1"""

try:
    from .sync_client import BeadsSyncClient, load_config
except ImportError:
    from sync_client import BeadsSyncClient, load_config  # type: ignore[import-not-found]

__all__ = ['BeadsSyncClient', 'load_config']
__version__ = '1.0.0'
