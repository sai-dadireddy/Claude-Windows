#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Unified Intent Detector & Skill Loader (v6.0)

CONSOLIDATES: skill_reminder, decision_reminder, beads_reminder,
              parallel_agent_reminder, memory_search, autonomous_brain, auto_rag,
              smart_router

This single script replaces 8+ separate hooks, reducing latency from ~1.5s to ~50ms.
All regex checks run in-memory in a single process.

Architecture:
- ADAPTIVE THINKING: Classifies tasks as FAST/DEEP/NORMAL to skip or enforce planning
- Smart Routing: Auto-detects persona (Coder/Architect/Researcher) and injects role
- JIT Documentation: Loads docs only when keywords detected (docs/ and refs/)
- Command Suggestions: Maps intent to /commands
- Behavioral Hints: Triggers memory saves, beads, skills
- Auto-Actions: Workflow suggestions (planning, cleanup, explore)
- Auto-RAG: Proactively injects relevant memories
- Circuit Breaker: Detects loops (same hint 3+ times) and stops

v6.0 Changes:
- Added ADAPTIVE THINKING protocol (FAST/DEEP/NORMAL modes)
- FAST mode: Simple tasks skip planning, execute immediately
- DEEP mode: Complex tasks require plan/bd create first
- NORMAL mode: Standard workflow, use judgment

v5.0 Changes:
- Merged AUTO_ACTIONS from autonomous_brain.py
- Added circuit breaker for loop detection
- Added refs/ JIT loading for CLAUDE.md optimization
"""

import sys
import json
import re
import subprocess
import tempfile
import os
from pathlib import Path
from datetime import datetime

# --- CONFIGURATION ---
HINT_FILE = Path.home() / ".claude" / "hints" / "current.txt"
DOCS_DIR = Path.home() / ".claude" / "docs"
REFS_DIR = Path.home() / ".claude" / "refs"
PROMPTS_DIR = Path.home() / ".claude" / "prompts"
SEMANTIC_SCRIPT = Path.home() / ".claude" / "scripts" / "semantic_memory.py"
HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"

# Add scripts dir to path for smart_router import
sys.path.insert(0, str(Path.home() / ".claude" / "scripts"))
try:
    import smart_router
    SMART_ROUTER_AVAILABLE = True
except ImportError:
    SMART_ROUTER_AVAILABLE = False

# Keep only last N hints to prevent file bloat
MAX_HINTS = 10
MIN_PROMPT_LEN = 15


def log(msg: str):
    """Log to hook log file."""
    try:
        HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HOOK_LOG, "a") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [IntentDetector] {msg}\n")
    except Exception:
        pass


# =============================================================================
# 0. ADAPTIVE THINKING (Complexity Layer)
# =============================================================================
# Categorizes tasks to skip planning for simple tasks, enforce it for complex ones

LOW_COMPLEXITY_PATTERNS = [
    r"(?i)\b(fix|typo|change|update|rename|move|delete|remove|add|set)\b",
    r"(?i)\b(color|text|button|style|css|margin|padding|font)\b",
    r"(?i)\b(log|print|debug|console)\b",
    r"(?i)\b(comment|uncomment|format|indent|lint)\b",
    r"(?i)\b(version|bump|upgrade pkg|install|uninstall)\b",
]

HIGH_COMPLEXITY_PATTERNS = [
    r"(?i)\b(scaffold|architect|refactor|design|implement|migrate)\b",
    r"(?i)\b(build|create|develop).*(system|service|feature|module|api)\b",
    r"(?i)\b(integrate|connect|wire up|hook up)\b",
    r"(?i)\b(authentication|authorization|auth|payment|checkout)\b",
    r"(?i)\b(database|schema|migration|orm|model)\b",
    r"(?i)\b(test suite|coverage|e2e|integration test)\b",
    r"(?i)\b(security|audit|vulnerability|penetration)\b",
    r"(?i)\b(performance|optimize|caching|scale)\b",
    r"(?i)\b(deploy|ci\/cd|pipeline|infrastructure)\b",
]

# Complexity score weights
COMPLEXITY_LOW_WEIGHT = -1
COMPLEXITY_HIGH_WEIGHT = 2


def calculate_complexity(prompt: str) -> tuple[str, int]:
    """
    Analyze prompt complexity to determine action mode.
    Returns (mode, score) where mode is 'FAST', 'DEEP', or 'NORMAL'.

    FAST = Simple task, skip planning, execute immediately
    DEEP = Complex task, create plan/task first, do not code yet
    NORMAL = Standard workflow, use judgment
    """
    score = 0
    low_matches = 0
    high_matches = 0

    # Count low complexity signals
    for pattern in LOW_COMPLEXITY_PATTERNS:
        if re.search(pattern, prompt):
            low_matches += 1
            score += COMPLEXITY_LOW_WEIGHT

    # Count high complexity signals
    for pattern in HIGH_COMPLEXITY_PATTERNS:
        if re.search(pattern, prompt):
            high_matches += 1
            score += COMPLEXITY_HIGH_WEIGHT

    # Word count heuristic - longer prompts often mean more complex tasks
    word_count = len(prompt.split())
    if word_count > 50:
        score += 1
    if word_count > 100:
        score += 1

    # Determine mode
    if score <= -1 and high_matches == 0:
        return ("FAST", score)
    elif score >= 2 or high_matches >= 2:
        return ("DEEP", score)
    else:
        return ("NORMAL", score)


# =============================================================================
# 1. JIT DOCUMENTATION (Knowledge Layer)
# =============================================================================
# Loads reference docs only when specific keywords appear
DOC_TRIGGERS = {
    r"(?i)\b(glm|multilingual|translate|chinese|japanese|korean)\b": "glm-orchestration.md",
    r"(?i)\b(context|large file|codebase|token limit|200k)\b": "model-prompting-guide.md",
    r"(?i)\b(parallel|simultaneously|agents|workmux|background)\b": "orchestration-guide.md",
    r"(?i)\b(route|router|model selection|compare|benchmark)\b": "model-routing-brain.md",
    r"(?i)\b(cost|price|budget|cheap|expensive|pricing)\b": "model-pricing-reference.md",
    r"(?i)\b(architect|stack|tech stack|standard|convention|best practice|pattern)\b": "architecture-overview.md",
}

# Reference guides (moved from CLAUDE.md for token efficiency)
REFS_TRIGGERS = {
    r"(?i)\b(honesty|lie|fabricate|verify|don't know|unsure)\b": "honesty-guide.md",
    r"(?i)\b(skill|systematic|debugging|tdd|test-driven|document skill)\b": "skills-guide.md",
    r"(?i)\b(memory|save decision|preference|semantic|remember)\b": "memory-guide.md",
    r"(?i)\b(beads|bd|issue|tracker|dependency|epic|blocker)\b": "beads-guide.md",
    r"(?i)\b(agent|parallel|workmux|worktree|subagent|autonomous)\b": "agents-guide.md",
    r"(?i)\b(mcp|context7|router|category|aws|github mcp)\b": "mcp-guide.md",
}

# =============================================================================
# 2. COMMAND SUGGESTIONS (Action Layer)
# =============================================================================
# Maps user intent to slash commands
COMMAND_TRIGGERS = {
    # -- Parallel Agents (Worktrees) --
    r"(?i)\b(background agent|spawn agent|worktree|new branch agent)\b": "/worktree-agent",
    r"(?i)\b(list agents|active tasks|background tasks|show worktrees)\b": "/worktree-list",
    r"(?i)\b(cleanup agents|remove worktrees|delete branches|prune)\b": "/worktree-cleanup",

    # -- Testing & QA --
    r"(?i)\b(tdd|test driven|red green refactor|write tests first)\b": "/tdd",
    r"(?i)\b(generate tests|add tests|test coverage|write tests for)\b": "/test-gen",
    r"(?i)\b(verify plan|check plan|validate specs|sanity check)\b": "/verify-plan",

    # -- Security & Audits --
    r"(?i)\b(audit|security check|vulnerability|scan)\b": "/security-audit",
    r"(?i)\b(review security|pen test|threat model)\b": "/security-review",
    r"(?i)\b(review pr|pull request|code review|diff)\b": "/review-pr",
    r"(?i)\b(ci|github action|pipeline|build failed)\b": "/gha",

    # -- Planning & Workflow --
    r"(?i)\b(plan|spec out|implementation plan|feature spec)\b": "/plan-feature",
    r"(?i)\b(rules|constitution|project rules)\b": "/project-rules",
    r"(?i)\b(summary|overview|context|onboard)\b": "/project-summary",
    r"(?i)\b(research|investigate|look into|find out about)\b": "/research",
    r"(?i)\b(brainstorm|ideas|options|alternatives)\b": "/brainstorm",
    r"(?i)\b(explore|find|locate|search code)\b": "/explore",
    r"(?i)\b(handoff|switch task|save state)\b": "/handoff",
    r"(?i)\b(what next|what to do|next step|blocked)\b": "/whats-next",

    # -- Session & Status --
    r"(?i)\b(save session|save progress|checkpoint session)\b": "/session-save",
    r"(?i)\b(resume|continue session|load session)\b": "/session-continue",
    r"(?i)\b(status|progress report|update status|tracker)\b": "/status",
    r"(?i)\b(optimize tokens|reduce context|token usage|too large)\b": "/token-optimize",
    r"(?i)\b(compact|summarize context)\b": "/compact-context",

    # -- Models & Memory --
    r"(?i)\b(save memory|remember this|save decision)\b": "/memory-save",
    r"(?i)\b(memory status|what do you know|recall)\b": "/memory-status",
    r"(?i)\b(route|which model|best model)\b": "/route",
    r"(?i)\b(compare|debate|ask models)\b": "/ask-models",
    r"(?i)\b(glm|zhipu)\b": "/glm",
}

# =============================================================================
# 3. BEHAVIORAL HINTS (Guidance Layer)
# =============================================================================
# Short reminders injected into context
HINT_TRIGGERS = {
    # Skills
    r"(?i)\b(debug|error|fail|exception|crash|broken)\b": "[skill] systematic-debugging: Reproduce -> Isolate -> Fix",
    r"(?i)\b(create|generate).*(pdf|docx|pptx|xlsx|document)\b": "[skill] Use document-skills tool (skill: \"pdf\", etc.)",

    # Memory
    r"(?i)\b(decision|choose|select|prefer|agreed|let's use|i prefer)\b": "[memory] SAVE TO MEMORY: decision detected - use memory_manager.py",

    # Beads
    r"(?i)\b(complex|multi-step|feature|epic|project|refactor)\b": "[beads] Complex task detected. Consider: bd create \"...\" -t feature",
    r"(?i)\b(dependencies|blocks|blocker|depends on)\b": "[beads] Dependencies detected. Use: bd dep add <child> <parent>",

    # Delegation (Pilot handoff)
    r"(?i)\b(pilot|scaffold|generate|build this|handle this|fix this for me|do this in background|while i work)\b": "[DELEGATE] Large task detected. DO NOT block user. Create: bd create \"...\" --labels pilot, then spawn worktree agent.",
}

# =============================================================================
# 4. AUTO-ACTIONS (From autonomous_brain.py - merged)
# =============================================================================
# Workflow suggestions based on task phase
AUTO_ACTIONS = {
    # Completion signals -> Suggest cleanup
    r"(?i)\b(finished|completed|done with|closing|merged)\b":
        "[action] CLEANUP: Task done. Run tests, then /worktree-cleanup",

    # New work -> Suggest planning
    r"(?i)\b(start|begin|initialize|new feature|implement)\b":
        "[action] PLANNING: Consider /plan-feature before coding",

    # Research needed -> Suggest exploration
    r"(?i)\b(investigate|research|understand|explore|analyze)\b":
        "[action] EXPLORE: Use Task(Explore) agent for codebase research",
}

# =============================================================================
# 5. MCP ROUTING (Via Router - Lazy Loading)
# =============================================================================
# Maps user intent to router_execute calls (saves ~60k tokens)
MCP_ROUTING = {
    # Context7 - Library documentation
    r"(?i)\b(react|vue|angular|next\.?js|express|fastapi|django|flask|rails)\b":
        "[router] context7: router_execute(mcp_name='context7', tool_name='resolve-library-id', arguments={...})",
    r"(?i)\b(how (do|does|to)|api|docs|documentation|syntax|example)\b.*\b(library|framework|package)\b":
        "[router] context7: router_execute(mcp_name='context7', tool_name='get-library-docs', ...)",

    # GitHub MCP - PRs, issues, repos
    r"(?i)\b(create|open|make).*(pr|pull request)\b":
        "[router] github: router_execute(mcp_name='github', tool_name='create_pull_request', ...)",
    r"(?i)\b(create|open|file).*(issue|bug report)\b":
        "[router] github: router_execute(mcp_name='github', tool_name='create_issue', ...)",
    r"(?i)\b(push|commit).*(github|remote|origin)\b":
        "[router] github: router_execute(mcp_name='github', tool_name='push_files', ...)",

    # Memory MCP - Entity relationships
    r"(?i)\b(relationship|depends on|connects to|relates to|links to)\b.*\b(entity|service|component)\b":
        "[router] memory: router_execute(mcp_name='memory', tool_name='create_relations', ...)",
    r"(?i)\b(knowledge graph|entity|store relationship)\b":
        "[router] memory: router_execute(mcp_name='memory', tool_name='create_entities', ...)",

    # Sequential Thinking - Complex reasoning
    r"(?i)\b(step by step|think through|analyze|reason|complex logic)\b":
        "[router] sequential-thinking: router_execute(mcp_name='sequential-thinking', tool_name='sequentialthinking', ...)",

    # Multi-Model - Compare/debate
    r"(?i)\b(compare models|get opinions|multiple perspectives|debate)\b":
        "[router] multi: router_execute(mcp_name='multi', tool_name='compare', ...)",
    r"(?i)\b(code review|security review|review this)\b":
        "[router] multi: router_execute(mcp_name='multi', tool_name='codereview', ...)",
    r"(?i)\b(gemini|gpt|glm|other model)\b":
        "[router] multi: router_execute(mcp_name='multi', tool_name='chat', arguments={'model': '...'})",

    # Code Index - Codebase search
    r"(?i)\b(index|search codebase|find in code|code search)\b":
        "[router] code-index: router_execute(mcp_name='code-index', tool_name='search_code_advanced', ...)",

    # --- MULTI-AI MODEL ROUTING ---
    # Large context (>200K tokens)
    r"(?i)\b(large (file|context|codebase)|million tokens|1m context|huge file)\b":
        "[router] multi: router_execute(..., arguments={'model': 'gemini-2.5-flash'})",

    # Multilingual / Chinese / Asian languages
    r"(?i)\b(chinese|japanese|korean|multilingual|translate|翻译|日本語|한국어)\b":
        "[router] multi: router_execute(..., arguments={'model': 'glm-4.7'})",

    # Deep reasoning / Math / Logic
    r"(?i)\b(math|reasoning|logic|prove|theorem|calculate|complex problem)\b":
        "[router] multi: router_execute(..., arguments={'model': 'deepseek-r1'})",

    # Code generation / Coding tasks
    r"(?i)\b(generate code|write code|coding|implement algorithm)\b":
        "[router] multi: router_execute(..., arguments={'model': 'qwen3-coder'})",

    # FREE models for simple tasks
    r"(?i)\b(free|cheap|budget|cost.effective|save money)\b":
        "[router] multi: FREE models via router_execute(..., arguments={'model': 'deepseek-v3.2|llama-405b|kimi-k2'})",

    # Vision / Images
    r"(?i)\b(image|vision|screenshot|diagram|visual|picture)\b":
        "[router] multi: router_execute(..., arguments={'model': 'pixtral-large'}) for vision",
}

# =============================================================================
# 6. AUTO-RAG TRIGGERS (Proactive Memory Search)
# =============================================================================
# These trigger automatic memory search and injection
AUTO_RAG_PATTERNS = [
    (r"(?i)\b(how did we|what was the decision|why did we choose)\b", "decision"),
    (r"(?i)\b(context for|background on|what is the architecture)\b", "architecture"),
    (r"(?i)\b(fix for|solution to|how to resolve|similar error)\b", "bug"),
    (r"(?i)\b(pattern for|how to implement|like we did|same approach)\b", "learning"),
]

# =============================================================================
# 7. CIRCUIT BREAKER (Loop Detection)
# =============================================================================
HISTORY_FILE = Path.home() / ".claude" / "hints" / "history.json"
MAX_REPEATS = 3  # Stop after same hint 3 times


def check_circuit_breaker(hints: list) -> tuple[list, bool]:
    """
    Check if we're in a loop (same hints repeated).
    Returns (filtered_hints, loop_detected).
    """
    if not hints:
        return hints, False

    try:
        history = []
        if HISTORY_FILE.exists():
            content = HISTORY_FILE.read_text().strip()
            if content:
                history = json.loads(content)[-20:]  # Keep last 20

        # Check for repeats
        hint_key = "|".join(sorted(hints))
        repeat_count = sum(1 for h in history if h == hint_key)

        # Update history
        history.append(hint_key)
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(history[-20:]))

        if repeat_count >= MAX_REPEATS:
            log(f"CIRCUIT BREAKER: '{hint_key[:50]}' repeated {repeat_count}x")
            return ["[STOP] Loop detected. Same action suggested 3+ times. ASK USER for direction."], True

    except Exception as e:
        log(f"Circuit breaker error: {e}")

    return hints, False


def search_memories(category: str, query: str) -> list:
    """Search semantic memory for relevant context."""
    if not SEMANTIC_SCRIPT.exists():
        return []
    try:
        result = subprocess.run(
            [sys.executable, str(SEMANTIC_SCRIPT), "search", "global", query],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0 and result.stdout.strip():
            memories = json.loads(result.stdout)
            return memories[:2]  # Limit to top 2
    except Exception:
        pass
    return []


def write_hints(hints: list):
    """Write hints to signal file using atomic writes for reliability."""
    if not hints:
        return

    try:
        HINT_FILE.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Read existing (keep last few)
        existing = []
        if HINT_FILE.exists():
            content = HINT_FILE.read_text().strip()
            if content:
                existing = content.split('\n')[-(MAX_HINTS - len(hints)):]

        # Add new hints
        new_lines = existing + [f"[{timestamp}] {h}" for h in hints]
        final_content = '\n'.join(new_lines[-MAX_HINTS:])

        # ATOMIC WRITE: Write to temp file first, then rename
        # This prevents race conditions where reader sees partial/empty file
        with tempfile.NamedTemporaryFile('w', delete=False, dir=HINT_FILE.parent, suffix='.tmp') as tf:
            tf.write(final_content)
            temp_name = tf.name

        # os.replace is atomic on POSIX systems
        os.replace(temp_name, HINT_FILE)
    except Exception:
        # Clean up temp file on error
        try:
            if 'temp_name' in locals():
                os.unlink(temp_name)
        except Exception:
            pass


def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")
    except Exception:
        sys.exit(0)

    # Skip very short prompts
    if len(prompt) < MIN_PROMPT_LEN:
        sys.exit(0)

    hints = []
    rag_context = []
    matched_count = 0
    terminal_parts = []  # For user-visible terminal output

    # =================================================================
    # ADAPTIVE THINKING: Calculate complexity first
    # =================================================================
    mode, complexity_score = calculate_complexity(prompt)

    if mode == "FAST":
        # FAST MODE: Simple task - skip planning, execute immediately
        hints.append("[MODE: FAST] Action: Skip planning. Execute command immediately. No bd create needed.")
        rag_context.append(
            "<adaptive-thinking mode=\"FAST\" score=\"{score}\">\n"
            "Simple task detected. EXECUTE DIRECTLY:\n"
            "- Do NOT create beads/issues\n"
            "- Do NOT write plans\n"
            "- Just make the change immediately\n"
            "</adaptive-thinking>".format(score=complexity_score)
        )
        log(f"FAST mode: score={complexity_score}")
        # For FAST mode, skip most other checks to reduce latency
        write_hints(hints)
        # Output to BOTH terminal and Claude
        output = {
            "systemMessage": f"[FAST] FAST mode (score: {complexity_score})",
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n".join(rag_context)
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    elif mode == "DEEP":
        # DEEP MODE: Complex task - create plan/task first
        hints.append("[MODE: DEEP] Action: Create a plan/task first. Do NOT code yet.")
        rag_context.append(
            "<adaptive-thinking mode=\"DEEP\" score=\"{score}\">\n"
            "Complex task detected. PLAN FIRST:\n"
            "1. Consider: bd create \"task description\" -t feature\n"
            "2. Or use /plan-feature to spec it out\n"
            "3. Break into subtasks before coding\n"
            "4. Check dependencies with bd ready\n"
            "</adaptive-thinking>".format(score=complexity_score)
        )
        log(f"DEEP mode: score={complexity_score}")
        matched_count += 1  # Count mode as a match

    # 1. Check JIT Documentation triggers (docs/ and refs/)
    doc_found = False
    for pattern, filename in DOC_TRIGGERS.items():
        if re.search(pattern, prompt):
            doc_path = DOCS_DIR / filename
            if doc_path.exists():
                hints.append(f"[doc] Load: cat {doc_path}")
                doc_found = True
            matched_count += 1
            break  # Only one doc per prompt

    # Check refs/ if no doc found
    if not doc_found:
        for pattern, filename in REFS_TRIGGERS.items():
            if re.search(pattern, prompt):
                ref_path = REFS_DIR / filename
                if ref_path.exists():
                    hints.append(f"[ref] Load: cat {ref_path}")
                matched_count += 1
                break  # Only one ref per prompt

    # 2. Check Command suggestions
    for pattern, cmd in COMMAND_TRIGGERS.items():
        if re.search(pattern, prompt):
            hints.append(f"[cmd] Suggestion: {cmd}")
            matched_count += 1
            break  # Only one command per prompt

    # 3. Check Behavioral hints
    for pattern, hint in HINT_TRIGGERS.items():
        if re.search(pattern, prompt):
            hints.append(hint)
            matched_count += 1

    # 4. Check Auto-Actions (workflow suggestions)
    for pattern, action in AUTO_ACTIONS.items():
        if re.search(pattern, prompt):
            hints.append(action)
            matched_count += 1
            break  # Only one action per prompt

    # 5. Check MCP Routing (explicit MCP tool guidance)
    for pattern, mcp_hint in MCP_ROUTING.items():
        if re.search(pattern, prompt):
            hints.append(mcp_hint)
            matched_count += 1
            break  # Only one MCP hint per prompt

    # 6. Check Auto-RAG triggers (proactive memory search)
    for pattern, category in AUTO_RAG_PATTERNS:
        if re.search(pattern, prompt):
            memories = search_memories(category, prompt)
            if memories:
                lines = [f"<auto-rag category=\"{category}\">"]
                for m in memories:
                    content = m.get("content", "")[:150]
                    sim = m.get("similarity", 0)
                    lines.append(f"  [{sim:.0%}] {content}")
                lines.append("</auto-rag>")
                rag_context.append("\n".join(lines))
                log(f"Auto-RAG: {category} - {len(memories)} memories")
            break  # Only one RAG query per prompt

    # 5. Smart Routing - Persona Injection (NEW)
    persona_injected = None
    if SMART_ROUTER_AVAILABLE:
        try:
            analysis = smart_router.analyze_task(prompt)
            prompt_file = analysis.get('prompt_file', 'coder.md')
            model = analysis.get('model', 'sonnet')
            confidence = analysis.get('confidence', 0)

            # Only inject persona if:
            # - Not the default coder persona
            # - High enough confidence (>75%)
            if prompt_file != 'coder.md' and confidence > 0.75:
                persona_path = PROMPTS_DIR / prompt_file
                if persona_path.exists():
                    persona_content = persona_path.read_text().strip()
                    # Inject persona as context (will appear in hookSpecificOutput)
                    persona_injected = prompt_file
                    rag_context.append(f"<persona-switch role=\"{prompt_file}\">\n{persona_content}\n</persona-switch>")
                    log(f"Smart Router: Injected {prompt_file} persona")

            # Advisory if different model would be better
            current_model = os.environ.get('ANTHROPIC_MODEL', 'sonnet').lower()
            if model != 'sonnet' and model not in current_model:
                if model == 'opus' and confidence > 0.85:
                    hints.append("[model] Complex task detected. Consider: export ANTHROPIC_MODEL=opus")
                elif model == 'gemini-2.5-flash' and confidence > 0.8:
                    hints.append("[model] Large context task. Consider: use /route or multi:chat gemini-2.5-flash")
                elif model == 'glm-4.7':
                    hints.append("[model] Multilingual detected. Consider: use /glm or multi:chat glm-4.7")

        except Exception as e:
            log(f"Smart Router error: {e}")

    # Apply circuit breaker before writing
    hints, loop_detected = check_circuit_breaker(hints)

    # Write hints to signal file
    write_hints(hints)

    # If loop detected, also inject warning into context
    if loop_detected:
        rag_context.append("<circuit-breaker>\nLoop detected: Same hints triggered 3+ times.\nSTOP and ask user for explicit direction.\n</circuit-breaker>")

    # Build terminal message
    terminal_parts = []
    if matched_count > 0 or persona_injected or mode != "NORMAL":
        log(f"Mode={mode} Matched {matched_count} patterns, {len(hints)} hints written")
        if mode == "DEEP":
            terminal_parts.append("[DEEP] DEEP mode")
        elif mode == "NORMAL" and matched_count > 0:
            terminal_parts.append("[NORMAL] NORMAL")
        if matched_count > 0:
            terminal_parts.append(f"{matched_count} matches")
        if persona_injected:
            terminal_parts.append(f"[PERSONA] {persona_injected.replace('.md', '')}")

    # Output to BOTH channels
    output = {}

    if terminal_parts:
        output["systemMessage"] = f"[FAST] Intent: {', '.join(terminal_parts)}"

    if rag_context:
        output["hookSpecificOutput"] = {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(rag_context)
        }

    if output:
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
