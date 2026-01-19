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

from .client import AgentLoaderClient

__all__ = ["AgentLoaderClient"]
__version__ = "1.0.0"
