#!/bin/bash
#
# Ralph Loop - Spawns fresh Claude Code instances for each iteration
# Based on Ryan Carson's implementation from ghuntley/how-to-ralph-wiggum
#
# Usage: ./ralph_loop.sh [prd.json] [max_iterations]
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRD_FILE="${1:-.ralph/prd.json}"
MAX_ITERATIONS="${2:-10}"
RALPH_DIR=".ralph"
PROGRESS_FILE="$RALPH_DIR/progress.txt"
LOG_FILE="$RALPH_DIR/loop.log"
ARCHIVE_DIR="$RALPH_DIR/archive"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[RALPH]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1" >> "$LOG_FILE"
}

# Initialize Ralph directory
init_ralph() {
    mkdir -p "$RALPH_DIR" "$ARCHIVE_DIR"

    if [ ! -f "$PRD_FILE" ]; then
        error "PRD file not found: $PRD_FILE"
        echo "Create a prd.json file first using: /prd-to-stories"
        exit 1
    fi

    # Initialize progress file
    if [ ! -f "$PROGRESS_FILE" ]; then
        echo "# Ralph Progress Log" > "$PROGRESS_FILE"
        echo "Started: $(date)" >> "$PROGRESS_FILE"
        echo "" >> "$PROGRESS_FILE"
    fi

    log "Initialized Ralph in $RALPH_DIR"
}

# Get next incomplete story from prd.json
get_next_story() {
    # Find first story where passes == false
    if command -v jq &> /dev/null; then
        jq -r '.stories[] | select(.passes == false) | .id' "$PRD_FILE" | head -1
    else
        # Fallback: grep for passes: false
        grep -B5 '"passes": false' "$PRD_FILE" | grep '"id"' | head -1 | sed 's/.*"id": "\([^"]*\)".*/\1/'
    fi
}

# Get story details
get_story_details() {
    local story_id="$1"
    if command -v jq &> /dev/null; then
        jq -r ".stories[] | select(.id == \"$story_id\")" "$PRD_FILE"
    else
        echo "Story: $story_id"
    fi
}

# Count remaining stories
count_remaining() {
    if command -v jq &> /dev/null; then
        jq -r '[.stories[] | select(.passes == false)] | length' "$PRD_FILE"
    else
        grep -c '"passes": false' "$PRD_FILE" || echo "0"
    fi
}

# Create system prompt for this iteration
create_system_prompt() {
    local story_id="$1"
    local iteration="$2"

    cat << EOF
You are an autonomous coding agent working on this project.

## Your Task

1. Read the PRD file: $PRD_FILE
2. Read the progress log: $PROGRESS_FILE
3. Focus on story: $story_id
4. Implement the story according to its acceptance criteria
5. Test your implementation
6. Commit your changes with a descriptive message
7. Update $PRD_FILE - set passes: true for this story
8. Update $PROGRESS_FILE with what you did

## Rules

- Complete ONE story per iteration
- Each story must pass ALL acceptance criteria before marking complete
- If you learn something important about the codebase, update agents.md in that folder
- If you hit a blocker, log it and move to the next story
- Run tests after implementation
- Commit with format: "feat(story-id): description"

## Progress Report Format

Append to $PROGRESS_FILE:

---
## Iteration $iteration - Story: $story_id
Thread: [timestamp]
Implemented: [what you built]
Files Changed: [list of files]
Tests: [pass/fail]
Learnings: [any insights for future iterations]
---

## Completion Signal

When done with this story, output exactly:
RALPH_ITERATION_COMPLETE

This signals the loop to continue to the next iteration.
EOF
}

# Run one iteration
run_iteration() {
    local iteration="$1"
    local story_id="$2"

    log "=== Iteration $iteration: $story_id ==="

    # Create temp file for system prompt
    local prompt_file=$(mktemp)
    create_system_prompt "$story_id" "$iteration" > "$prompt_file"

    # Archive the prompt
    cp "$prompt_file" "$ARCHIVE_DIR/iteration-${iteration}-prompt.txt"

    # Run Claude Code with the prompt
    # Using --print for non-interactive mode
    # Using --dangerously-skip-permissions for autonomous operation
    log "Starting Claude Code for story: $story_id"

    # Run Claude and capture output
    local output_file="$ARCHIVE_DIR/iteration-${iteration}-output.txt"

    if command -v claude &> /dev/null; then
        # Use claude command directly
        claude --print --dangerously-skip-permissions \
            --system-prompt "$(cat $prompt_file)" \
            "Implement story $story_id from $PRD_FILE. Follow the system instructions exactly." \
            2>&1 | tee "$output_file"
    else
        # Fallback: just show what would be run
        log "Claude command not found. Would run:"
        echo "claude --print --dangerously-skip-permissions --system-prompt '...' 'Implement story $story_id'"
        echo "RALPH_ITERATION_COMPLETE" > "$output_file"
    fi

    # Check if iteration completed
    if grep -q "RALPH_ITERATION_COMPLETE" "$output_file"; then
        success "Iteration $iteration completed"
        return 0
    else
        error "Iteration $iteration did not complete cleanly"
        return 1
    fi
}

# Main loop
main() {
    log "Starting Ralph Loop"
    log "PRD: $PRD_FILE"
    log "Max iterations: $MAX_ITERATIONS"

    init_ralph

    local iteration=1

    while [ $iteration -le $MAX_ITERATIONS ]; do
        # Get next story
        local story_id=$(get_next_story)

        if [ -z "$story_id" ]; then
            success "All stories complete!"
            break
        fi

        local remaining=$(count_remaining)
        log "Stories remaining: $remaining"

        # Run iteration
        if run_iteration $iteration "$story_id"; then
            ((iteration++))
        else
            log "Iteration failed, continuing anyway..."
            ((iteration++))
        fi

        # Small delay between iterations
        sleep 2
    done

    if [ $iteration -gt $MAX_ITERATIONS ]; then
        log "Reached max iterations ($MAX_ITERATIONS)"
    fi

    # Final status
    local final_remaining=$(count_remaining)
    if [ "$final_remaining" -eq 0 ]; then
        success "FEATURE_COMPLETE - All stories implemented!"
    else
        log "Finished with $final_remaining stories remaining"
    fi

    # Archive the run
    local archive_name="ralph-run-$(date '+%Y%m%d-%H%M%S')"
    if [ -d "$ARCHIVE_DIR" ]; then
        log "Run archived to: $ARCHIVE_DIR"
    fi
}

# Help
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    cat << EOF
Ralph Loop - Autonomous Feature Builder

Usage: ./ralph_loop.sh [prd.json] [max_iterations]

Arguments:
  prd.json        Path to PRD JSON file (default: .ralph/prd.json)
  max_iterations  Maximum iterations to run (default: 10)

Setup:
  1. Create PRD: Use /prd skill to generate PRD markdown
  2. Convert: Use /prd-to-stories to create prd.json
  3. Run: ./ralph_loop.sh

Example:
  ./ralph_loop.sh .ralph/prd.json 15

The script will:
  - Read user stories from prd.json
  - Spawn fresh Claude Code instance for each story
  - Track progress in .ralph/progress.txt
  - Archive each iteration's output
  - Stop when all stories pass or max iterations reached
EOF
    exit 0
fi

# Run
main
