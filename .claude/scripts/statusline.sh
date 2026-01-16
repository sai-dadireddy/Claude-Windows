#!/bin/bash

# Simple status line - shows model and context usage only
# Based on shanraisshan/claude-code-status-line (2.1.6+)

data=$(cat)

# Get model name
model=$(echo "$data" | jq -r '.model.display_name // .model.id // "unknown"')

# Get context info
max_ctx=$(echo "$data" | jq -r '.context_window.context_window_size // 200000')
used_pct=$(echo "$data" | jq -r '.context_window.used_percentage // empty')

# Color codes
BLUE='\033[34m'
RED='\033[31m'
YELLOW='\033[33m'
GREEN='\033[32m'
RESET='\033[0m'

# Format context display
if [ -z "$used_pct" ] || [ "$used_pct" = "null" ]; then
    # Loading state - empty circles
    context_info="○○○○○○○○○○ loading..."
else
    pct=$(printf "%.0f" "$used_pct" 2>/dev/null || echo "$used_pct")
    [ "$pct" -gt 100 ] 2>/dev/null && pct=100

    # Calculate tokens in k
    used_k=$(( max_ctx * pct / 100 / 1000 ))
    max_k=$(( max_ctx / 1000 ))

    # Build circle bar (10 segments)
    bar=""
    filled=$(( pct / 10 ))

    # Color based on usage: green < 60, yellow < 80, red >= 80
    if [ "$pct" -ge 80 ]; then
        COLOR="$RED"
    elif [ "$pct" -ge 60 ]; then
        COLOR="$YELLOW"
    else
        COLOR="$GREEN"
    fi

    for i in 0 1 2 3 4 5 6 7 8 9; do
        if [ "$i" -lt "$filled" ]; then
            bar="${bar}${COLOR}●${RESET}"
        else
            bar="${bar}○"
        fi
    done

    context_info="${bar} ${used_k}k/${max_k}k (${pct}%)"
fi

# Output: Model | Context
printf '%b\n' "${model} | ${context_info}"
