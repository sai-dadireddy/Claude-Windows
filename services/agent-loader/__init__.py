"""
Agent Loader Client

A client for the sherpa-agent-loader Lambda that provides lazy loading
of agent prompts from S3.

Usage:
    from services.agent_loader import AgentLoaderClient

    client = AgentLoaderClient()
    agents = client.list_agents()
    agent = client.get_agent("lead-architect")
"""

try:
    from .client import AgentLoaderClient
except ImportError:
    # Handle case when running standalone (e.g., pytest discovery)
    try:
        from client import AgentLoaderClient
    except ImportError:
        AgentLoaderClient = None

__all__ = ["AgentLoaderClient"]
__version__ = "1.0.0"
