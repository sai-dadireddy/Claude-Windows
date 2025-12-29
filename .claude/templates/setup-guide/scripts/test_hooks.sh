#!/bin/bash
# Hook Test Script - Run this to verify all hooks are working
# Usage: ~/.claude/scripts/test_hooks.sh

HOOKS_DIR="$HOME/.claude/hooks"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           CLAUDE CODE HOOKS TEST SUITE                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: Parallel Work Detection
echo -e "${YELLOW}▶ TEST 1: Parallel Work Detection${NC}"
result=$(echo '{"prompt": "implement 5 features in parallel"}' | python3 "$HOOKS_DIR/parallel_agent_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "parallel-agent-guide"; then
    echo -e "${GREEN}  ✓ Parallel work → Template injected${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 2: Model Routing - Multilingual
echo -e "${YELLOW}▶ TEST 2: Model Routing (Multilingual)${NC}"
result=$(echo '{"prompt": "write code with Chinese comments"}' | python3 "$HOOKS_DIR/parallel_agent_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "glm-4.7"; then
    echo -e "${GREEN}  ✓ Multilingual → Route to GLM 4.7${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 3: Model Routing - FREE
echo -e "${YELLOW}▶ TEST 3: Model Routing (FREE/Cheap)${NC}"
result=$(echo '{"prompt": "what is the cheapest way to do this"}' | python3 "$HOOKS_DIR/parallel_agent_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "deepseek"; then
    echo -e "${GREEN}  ✓ Cheap/Free → Route to DeepSeek${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 4: Model Routing - Large Context
echo -e "${YELLOW}▶ TEST 4: Model Routing (Large Context)${NC}"
result=$(echo '{"prompt": "analyze the entire codebase with 1 million tokens"}' | python3 "$HOOKS_DIR/parallel_agent_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "gemini"; then
    echo -e "${GREEN}  ✓ Large context → Route to Gemini${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 5: Skill Reminder - Debug
echo -e "${YELLOW}▶ TEST 5: Skill Reminder (Debug)${NC}"
result=$(echo '{"prompt": "debug this authentication error"}' | python3 "$HOOKS_DIR/skill_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "systematic-debugging"; then
    echo -e "${GREEN}  ✓ Debug task → systematic-debugging skill${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 6: Skill Reminder - PDF
echo -e "${YELLOW}▶ TEST 6: Skill Reminder (PDF)${NC}"
result=$(echo '{"prompt": "create a PDF report"}' | python3 "$HOOKS_DIR/skill_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "pdf"; then
    echo -e "${GREEN}  ✓ PDF task → pdf skill${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 7: Skill Reminder - TDD
echo -e "${YELLOW}▶ TEST 7: Skill Reminder (TDD)${NC}"
result=$(echo '{"prompt": "write unit tests for this module"}' | python3 "$HOOKS_DIR/skill_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "tdd"; then
    echo -e "${GREEN}  ✓ Testing → /tdd command${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 8: Beads Reminder
echo -e "${YELLOW}▶ TEST 8: Beads Reminder (Complex Task)${NC}"
result=$(echo '{"prompt": "implement a complete authentication system with multiple steps and dependencies", "cwd": "/tmp"}' | python3 "$HOOKS_DIR/beads_reminder.py" 2>/dev/null)
if echo "$result" | grep -q "beads"; then
    echo -e "${GREEN}  ✓ Complex task → Beads reminder${NC}"
else
    echo "  ✗ Not triggered"
fi

# Test 9: Session Tracking
echo -e "${YELLOW}▶ TEST 9: Session Tracking${NC}"
rm -f "$HOME/.claude/logs/session_activity.json"
for i in 1 2 3 4 5; do
    echo '{"tool_name": "Edit", "tool_input": {"file_path": "/test/file.py"}, "tool_response": {}, "cwd": "/tmp"}' | python3 "$HOOKS_DIR/auto_capture_memory.py" 2>/dev/null
done
if [ -f "$HOME/.claude/logs/session_activity.json" ]; then
    count=$(cat "$HOME/.claude/logs/session_activity.json" | grep -o '"significant_count": [0-9]*' | grep -o '[0-9]*')
    echo -e "${GREEN}  ✓ Session tracking active (${count} actions tracked)${NC}"
else
    echo "  ✗ Not tracking"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    WHAT YOU'LL SEE                         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "When you type prompts, Claude sees these reminders automatically:"
echo ""
echo -e "${YELLOW}Your prompt:${NC} 'debug this error'"
echo -e "${GREEN}Claude sees:${NC} <skill-reminder>→ systematic-debugging: Root-cause analysis</skill-reminder>"
echo ""
echo -e "${YELLOW}Your prompt:${NC} 'implement 5 features in parallel'"
echo -e "${GREEN}Claude sees:${NC} <parallel-agent-guide>TASK/DIRECTORY/CREATE/VERIFY template</parallel-agent-guide>"
echo ""
echo -e "${YELLOW}Your prompt:${NC} 'cheapest way to analyze this'"
echo -e "${GREEN}Claude sees:${NC} → Route to deepseek: FREE via Ollama"
echo ""
echo -e "${YELLOW}After 15+ edits:${NC}"
echo -e "${GREEN}You see:${NC} 💾 Big session! 15 actions - Consider saving with memory system"
echo ""
echo -e "${BLUE}All hooks are automatic - no action needed from you!${NC}"
