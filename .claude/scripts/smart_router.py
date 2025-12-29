#!/usr/bin/env python3
"""
Smart Router: Analyzes a task to determine Model, Strategy, and Prompt.

Usage:
    python3 smart_router.py "Task description"
    python3 smart_router.py --json "Task description"  # Machine-readable output

Models (2025):
- sonnet: Claude Sonnet 4 - Fast coding, default
- opus: Claude Opus 4.5 - Deep reasoning, architecture
- gemini-2.5-flash: Gemini - 1M context, research
- glm-4.7: GLM - Multilingual, Chinese/Japanese/Korean
"""

import sys
import json
import re


def analyze_task(task: str) -> dict:
    """Analyze task to determine optimal model, strategy, and persona."""
    task_lower = task.lower()

    # Defaults
    config = {
        "model": "sonnet",
        "strategy": "SERIAL",
        "prompt_file": "coder.md",
        "reason": "Default coding task",
        "confidence": 0.8
    }

    # --- 1. DECIDE STRATEGY (Parallel vs Serial) ---
    parallel_triggers = [
        'independent', 'parallel', 'multiple', 'all files', 'batch',
        'simultaneously', 'concurrent', 'each file', 'every module',
        'in parallel', 'at the same time'
    ]
    serial_triggers = [
        'then', 'after', 'depends on', 'first', 'before',
        'sequential', 'step by step', 'one by one'
    ]

    parallel_score = sum(1 for t in parallel_triggers if t in task_lower)
    serial_score = sum(1 for t in serial_triggers if t in task_lower)

    if parallel_score > serial_score and parallel_score > 0:
        config['strategy'] = "PARALLEL"
        config['reason'] = f"Detected parallelizable workload ({parallel_score} triggers)"

    # --- 2. DECIDE MODEL & PROMPT ---

    # Complex Architecture -> Opus 4.5
    architect_triggers = [
        'architect', 'design', 'plan', 'complex', 'security', 'audit',
        'refactor entire', 'system design', 'trade-off', 'scalability',
        'migration strategy', 'breaking change'
    ]
    if any(t in task_lower for t in architect_triggers):
        config['model'] = "opus"
        config['prompt_file'] = "architect.md"
        config['reason'] = "High complexity requiring Opus reasoning"
        config['confidence'] = 0.9

    # Massive Context/Research -> Gemini 2.5 Flash
    elif any(t in task_lower for t in [
        'read all', 'analyze codebase', 'summarize', 'find in docs',
        'entire repo', 'all documentation', 'full context', 'scan everything'
    ]):
        config['model'] = "gemini-2.5-flash"
        config['prompt_file'] = "researcher.md"
        config['reason'] = "Heavy context load - using 1M token model"
        config['confidence'] = 0.85

    # Multilingual -> GLM 4.7
    elif any(t in task_lower for t in [
        'chinese', 'japanese', 'korean', 'multilingual', 'translate',
        'i18n', 'internationalization', 'localization', 'l10n'
    ]):
        config['model'] = "glm-4.7"
        config['prompt_file'] = "coder.md"
        config['reason'] = "Multilingual task - using GLM"
        config['confidence'] = 0.9

    # Quick/Simple -> Stay with Sonnet (already default)
    elif any(t in task_lower for t in [
        'fix', 'bug', 'typo', 'small', 'quick', 'simple', 'minor'
    ]):
        config['confidence'] = 0.95
        config['reason'] = "Simple task - fast Sonnet execution"

    return config


def format_human(config: dict) -> str:
    """Format output for human reading."""
    return f"""
Smart Router Decision:
  Model:    {config['model']}
  Strategy: {config['strategy']}
  Persona:  {config['prompt_file']}
  Reason:   {config['reason']}
  Confidence: {config['confidence']:.0%}
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: smart_router.py [--json] 'Task description'", file=sys.stderr)
        sys.exit(1)

    # Check for --json flag
    json_output = '--json' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--json']

    task_desc = ' '.join(args) if args else ""
    result = analyze_task(task_desc)

    if json_output:
        print(json.dumps(result))
    else:
        print(format_human(result))


if __name__ == "__main__":
    main()
