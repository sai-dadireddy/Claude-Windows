#!/usr/bin/env python3
"""
GLM Query Script - Execute queries against GLM 4.7

Usage:
    python glm-query.py "Your prompt here"
    python glm-query.py --thinking 10000 "Complex task"
    python glm-query.py --model glm-4.6 "Simple query"
"""

import argparse
import json
import os
import sys

def query_glm(prompt: str, model: str = "glm-4.7", thinking_budget: int = 0):
    """Query GLM via the multi MCP router"""

    # Build arguments for router
    args = {
        "model": model,
        "content": prompt
    }

    if thinking_budget > 0:
        args["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}

    # Output the router command for Claude to execute
    router_call = {
        "mcp_name": "multi",
        "tool_name": "chat",
        "arguments": args
    }

    print(f"Execute via router:")
    print(f"router_execute({json.dumps(router_call, indent=2)})")

    return router_call

def main():
    parser = argparse.ArgumentParser(description="Query GLM models")
    parser.add_argument("prompt", help="The prompt to send to GLM")
    parser.add_argument("--model", default="glm-4.7",
                        choices=["glm-4.7", "glm-4.6", "glm-4.5-air"],
                        help="Model to use")
    parser.add_argument("--thinking", type=int, default=0,
                        help="Thinking budget in tokens (0 = disabled)")

    args = parser.parse_args()

    query_glm(args.prompt, args.model, args.thinking)

if __name__ == "__main__":
    main()
