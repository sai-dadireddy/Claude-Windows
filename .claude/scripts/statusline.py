#!/usr/bin/env python3
"""
Custom Claude Code Status Line
Shows: Model | Context % (color-coded) | Cost estimate
Accounts for MCP/tool overhead for accurate percentage
"""
import json
import sys
import os

# ANSI color codes
BLUE = "\033[34m"
YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Overhead estimate for MCP tools and system prompts (tokens)
# Adjust based on your setup - more MCPs = more overhead
MCP_OVERHEAD = 15000  # ~15K for router + tools definitions

def get_color(percentage):
    """Color based on context usage"""
    if percentage < 60:
        return GREEN
    elif percentage < 75:
        return BLUE
    elif percentage < 85:
        return YELLOW
    else:
        return RED

def format_tokens(tokens):
    """Format token count (e.g., 52K, 1.2M)"""
    if tokens >= 1_000_000:
        return f"{tokens/1_000_000:.1f}M"
    elif tokens >= 1000:
        return f"{tokens//1000}K"
    return str(tokens)

def estimate_cost(input_tokens, output_tokens, model):
    """Estimate cost based on model pricing"""
    # Pricing per 1M tokens (Jan 2026)
    pricing = {
        "opus": {"input": 15.00, "output": 75.00},
        "sonnet": {"input": 3.00, "output": 15.00},
        "haiku": {"input": 0.25, "output": 1.25},
    }

    model_key = "sonnet"  # default
    if "opus" in model.lower():
        model_key = "opus"
    elif "haiku" in model.lower():
        model_key = "haiku"

    input_cost = (input_tokens / 1_000_000) * pricing[model_key]["input"]
    output_cost = (output_tokens / 1_000_000) * pricing[model_key]["output"]
    return input_cost + output_cost

def main():
    try:
        # Read status data from stdin
        data = json.load(sys.stdin)

        # Extract context window info
        ctx = data.get("context_window", {})
        model = data.get("model", "unknown")

        # Get token counts
        total_input = ctx.get("total_input_tokens", 0)
        total_output = ctx.get("total_output_tokens", 0)
        context_size = ctx.get("context_window_size", 200000)

        # Calculate actual usage including overhead
        actual_usage = total_input + total_output + MCP_OVERHEAD
        actual_percentage = min(99, int((actual_usage / context_size) * 100))

        # Get official percentage for comparison
        official_pct = ctx.get("used_percentage", 0)
        remaining_pct = ctx.get("remaining_percentage", 100)

        # Estimate cost
        cost = estimate_cost(total_input, total_output, model)

        # Format model name (short)
        model_short = model.split("-")[0].capitalize() if model else "?"
        if "opus" in model.lower():
            model_short = "Opus"
        elif "sonnet" in model.lower():
            model_short = "Sonnet"
        elif "haiku" in model.lower():
            model_short = "Haiku"

        # Build status line
        color = get_color(actual_percentage)

        # Progress bar (10 chars)
        filled = actual_percentage // 10
        bar = "=" * filled + "-" * (10 - filled)

        # Output format: Model | [====----] 45% | $0.12
        status = f"{GRAY}{model_short}{RESET} {color}[{bar}]{RESET} {color}{actual_percentage}%{RESET} {GRAY}${cost:.2f}{RESET}"

        print(status)

    except Exception as e:
        # Fallback on error
        print(f"{GRAY}Claude Code{RESET}")

if __name__ == "__main__":
    main()
