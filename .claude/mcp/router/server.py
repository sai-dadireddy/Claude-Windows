#!/usr/bin/env python3
"""
MCP Router - Lazy loading MCP proxy for Claude Code

This router exposes 4 lightweight tools that proxy to backend MCPs on demand,
saving ~60k tokens by not loading all MCP tool definitions into context.

Architecture:
  Claude -> router (4 tools, ~2.4k tokens) -> backend MCPs (loaded on demand)
"""

import asyncio
import json
import subprocess
import os
from typing import Any
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Windows path helpers
NPX = "C:/Program Files/nodejs/npx.cmd"
UVX = os.path.expanduser("~/.local/bin/uvx.exe")
NODE = "C:/Program Files/nodejs/node.exe"

# Backend MCP configurations - these are NOT loaded into Claude's context
BACKEND_MCPS = {
    "context7": {
        "description": "Library documentation and API references",
        "command": [NPX, "-y", "@upstash/context7-mcp"],
        "tools": ["resolve-library-id", "get-library-docs"],
        "triggers": ["library", "docs", "documentation", "api", "npm", "package"],
    },
    "github": {
        "description": "GitHub operations: PRs, issues, repos",
        "command": [NPX, "-y", "@modelcontextprotocol/server-github"],
        "tools": [
            "create_pull_request", "create_issue", "get_file_contents",
            "search_repositories", "list_issues", "get_pull_request",
            "create_branch", "push_files", "fork_repository"
        ],
        "triggers": ["github", "pr", "pull request", "issue", "repo", "repository"],
    },
    "memory": {
        "description": "Knowledge graph for entity relationships",
        "command": [NPX, "-y", "@modelcontextprotocol/server-memory"],
        "tools": [
            "create_entities", "create_relations", "add_observations",
            "delete_entities", "search_nodes", "read_graph", "open_nodes"
        ],
        "triggers": ["memory", "entity", "relationship", "knowledge graph"],
    },
    "sequential-thinking": {
        "description": "Multi-step reasoning and problem solving",
        "command": [NPX, "-y", "@modelcontextprotocol/server-sequential-thinking"],
        "tools": ["sequentialthinking"],
        "triggers": ["reasoning", "think step", "complex problem", "analyze"],
    },
    "multi": {
        "description": "Multi-model queries: chat, compare, debate, code review",
        "command": [os.path.expanduser("~/.claude/mcp/multi_mcp/.venv/Scripts/python.exe"), "-m", "multi_mcp.server"],
        "tools": ["chat", "compare", "debate", "codereview", "models", "version"],
        "triggers": ["multi-model", "compare models", "code review", "glm", "gemini", "gpt"],
    },
    "playwright": {
        "description": "Browser automation and testing",
        "command": [NPX, "-y", "@executeautomation/playwright-mcp-server"],
        "tools": [
            "playwright_navigate", "playwright_screenshot", "playwright_click",
            "playwright_fill", "playwright_evaluate", "playwright_close"
        ],
        "triggers": ["browser", "playwright", "screenshot", "navigate", "automation"],
    },
    "code-index": {
        "description": "Code indexing and advanced search",
        "command": [UVX, "code-index-mcp"],
        "tools": [
            "set_project_path", "search_code_advanced", "find_files",
            "get_file_summary", "refresh_index", "build_deep_index"
        ],
        "triggers": ["index", "code search", "find files", "codebase"],
    },
    "memory-bridge": {
        "description": "AWS memory bridge: save/search/retrieve memories with local cache + AWS backend",
        "command": ["python", "-m", "memory_bridge"],
        "cwd": "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/claudecodeshared/services/mcp-bridge",
        "tools": [
            "memory_save", "memory_search", "memory_retrieve",
            "memory_sync", "memory_stats"
        ],
        "triggers": ["memory save", "memory search", "memories", "remember", "recall", "semantic search"],
        "env": {
            "SHERPA_MEMORY_API": os.environ.get("SHERPA_MEMORY_API", ""),
            "SHERPA_KB_ID": os.environ.get("SHERPA_KB_ID", ""),
            "AWS_PROFILE": os.environ.get("AWS_PROFILE", "sherpa"),
        }
    },
    "skill-seekers": {
        "description": "Automated skill creation: scrape docs, enhance, package, upload to Claude, install to agents",
        "command": ["skill-seekers", "mcp"],
        "tools": [
            "list_configs", "generate_config", "fetch_config", "validate_config",
            "scrape_docs", "scrape_github", "scrape_pdf", "estimate_pages",
            "enhance_skill", "package_skill", "upload_skill",
            "install_skill", "install_agent", "split_config", "generate_router"
        ],
        "triggers": ["skill", "scrape docs", "create skill", "package skill", "install skill"],
    },
    "excel-bridge": {
        "description": "Excel file operations: read, write, analyze, find values in xlsx files",
        "command": [NPX, "-y", "excel-mcp-server"],
        "tools": [
            "read_excel", "write_excel", "analyze_excel", "find_in_excel",
            "create_workbook", "list_sheets"
        ],
        "triggers": ["excel", "xlsx", "spreadsheet", "workbook", "cells"],
    },
    "fetchaller": {
        "description": "Fetch URLs without permission prompts, browse/search Reddit",
        "command": [NODE, "C:/Users/SainathreddyDadiredd/.claude/mcp/fetchaller-mcp/index.js"],
        "tools": ["fetch", "browse_reddit", "search_reddit"],
        "triggers": ["fetch url", "reddit", "browse", "http get"],
    },
    "chrome-devtools": {
        "description": "Chrome DevTools: debug pages, console logs, network, performance profiling, screenshots",
        "command": [NPX, "-y", "chrome-devtools-mcp@latest"],
        "tools": [
            "browser_navigate", "browser_click", "browser_type", "browser_screenshot",
            "browser_console_messages", "browser_network_requests", "browser_evaluate",
            "browser_scroll", "browser_select_option", "browser_hover", "browser_wait_for",
            "browser_tabs", "browser_tab_new", "browser_tab_select", "browser_tab_close",
            "browser_resize", "browser_refresh", "browser_back", "browser_forward"
        ],
        "triggers": ["devtools", "console", "network", "performance", "chrome debug", "browser"],
    },
}

# Cache for running MCP processes
_mcp_processes: dict[str, subprocess.Popen] = {}


def get_backend_summary() -> str:
    """Generate a summary of available backend MCPs."""
    lines = ["Available MCP backends:"]
    for name, config in BACKEND_MCPS.items():
        tools_preview = ", ".join(config["tools"][:3])
        if len(config["tools"]) > 3:
            tools_preview += f" (+{len(config['tools'])-3} more)"
        lines.append(f"  - {name}: {config['description']}")
        lines.append(f"    Tools: {tools_preview}")
        lines.append(f"    Triggers: {', '.join(config['triggers'][:3])}")
    return "\n".join(lines)


def analyze_intent(query: str) -> dict[str, Any]:
    """Analyze query to suggest which MCP to use."""
    query_lower = query.lower()
    matches = []

    for name, config in BACKEND_MCPS.items():
        score = 0
        matched_triggers = []
        for trigger in config["triggers"]:
            if trigger.lower() in query_lower:
                score += 1
                matched_triggers.append(trigger)

        # Also check tool names
        for tool in config["tools"]:
            if tool.lower().replace("_", " ") in query_lower or tool.lower().replace("-", " ") in query_lower:
                score += 2
                matched_triggers.append(f"tool:{tool}")

        if score > 0:
            matches.append({
                "mcp": name,
                "score": score,
                "matched": matched_triggers,
                "description": config["description"],
                "tools": config["tools"],
            })

    matches.sort(key=lambda x: x["score"], reverse=True)

    return {
        "query": query,
        "recommendations": matches[:3] if matches else [],
        "suggestion": matches[0]["mcp"] if matches else None,
        "all_backends": list(BACKEND_MCPS.keys()),
    }


async def execute_mcp_tool(mcp_name: str, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Execute a tool on a backend MCP server."""
    if mcp_name not in BACKEND_MCPS:
        return {"error": f"Unknown MCP: {mcp_name}", "available": list(BACKEND_MCPS.keys())}

    config = BACKEND_MCPS[mcp_name]

    # Build the MCP tool call request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        }
    }

    try:
        # Start MCP server process if not running
        env = os.environ.copy()

        # Special handling for github (needs GITHUB_TOKEN)
        if mcp_name == "github" and "GITHUB_TOKEN" not in env:
            token_file = Path.home() / ".config" / "gh" / "hosts.yml"
            # Try to get token from gh CLI
            try:
                result = subprocess.run(
                    ["gh", "auth", "token"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    env["GITHUB_TOKEN"] = result.stdout.strip()
            except Exception:
                pass

        # Apply custom environment variables from config
        if "env" in config:
            env.update(config["env"])

        # Determine working directory
        cwd = config.get("cwd")

        # Run the MCP server and communicate
        process = subprocess.Popen(
            config["command"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            cwd=cwd,
        )

        # Send initialization
        init_request = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp-router", "version": "1.0.0"}
            }
        }

        # Communicate with the MCP server
        stdin_data = json.dumps(init_request) + "\n" + json.dumps(request) + "\n"
        stdout, stderr = process.communicate(input=stdin_data.encode(), timeout=30)

        # Parse response
        responses = stdout.decode().strip().split("\n")
        for resp_line in responses:
            if resp_line:
                try:
                    resp = json.loads(resp_line)
                    if resp.get("id") == 1:  # Our tool call response
                        if "result" in resp:
                            return {"success": True, "result": resp["result"]}
                        elif "error" in resp:
                            return {"success": False, "error": resp["error"]}
                except json.JSONDecodeError:
                    continue

        return {"success": False, "error": "No valid response from MCP", "stderr": stderr.decode()[:500]}

    except subprocess.TimeoutExpired:
        return {"error": f"MCP {mcp_name} timed out"}
    except Exception as e:
        return {"error": f"Failed to execute: {str(e)}"}


# Create the MCP server
server = Server("mcp-router")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List the router's 4 lightweight tools."""
    return [
        Tool(
            name="router_analyze_intent",
            description="Analyze a query to determine which MCP backend to use. Returns recommendations based on keywords and tool names.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's request or task description to analyze"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="router_list_categories",
            description="List all available MCP backends with their descriptions, tools, and trigger keywords.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="router_load_toolset",
            description="Get detailed tool information for a specific MCP backend. Use this to see available tools before calling router_execute.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mcp_name": {
                        "type": "string",
                        "description": "Name of the MCP backend",
                        "enum": list(BACKEND_MCPS.keys())
                    }
                },
                "required": ["mcp_name"]
            }
        ),
        Tool(
            name="router_execute",
            description="Execute a tool on a backend MCP server. The MCP is loaded on-demand, keeping context lean.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mcp_name": {
                        "type": "string",
                        "description": "Name of the MCP backend to use",
                        "enum": list(BACKEND_MCPS.keys())
                    },
                    "tool_name": {
                        "type": "string",
                        "description": "Name of the tool to execute"
                    },
                    "arguments": {
                        "type": "object",
                        "description": "Arguments to pass to the tool",
                        "additionalProperties": True
                    }
                },
                "required": ["mcp_name", "tool_name"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""

    if name == "router_analyze_intent":
        result = analyze_intent(arguments.get("query", ""))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "router_list_categories":
        return [TextContent(type="text", text=get_backend_summary())]

    elif name == "router_load_toolset":
        mcp_name = arguments.get("mcp_name", "")
        if mcp_name not in BACKEND_MCPS:
            return [TextContent(type="text", text=f"Unknown MCP: {mcp_name}. Available: {list(BACKEND_MCPS.keys())}")]

        config = BACKEND_MCPS[mcp_name]
        info = {
            "name": mcp_name,
            "description": config["description"],
            "tools": config["tools"],
            "triggers": config["triggers"],
            "usage": f"Use router_execute with mcp_name='{mcp_name}' and tool_name='<tool>'"
        }
        return [TextContent(type="text", text=json.dumps(info, indent=2))]

    elif name == "router_execute":
        mcp_name = arguments.get("mcp_name", "")
        tool_name = arguments.get("tool_name", "")
        tool_args = arguments.get("arguments", {})

        result = await execute_mcp_tool(mcp_name, tool_name, tool_args)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main_async():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Entry point."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
