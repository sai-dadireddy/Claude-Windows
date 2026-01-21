#!/usr/bin/env python3
"""
Router Learning System: Tracks routing decisions and outcomes to improve future routing.

Usage:
    # Record a routing outcome
    python router_learning.py record --task "fix auth bug" --model sonnet --agent coder --outcome success
    python router_learning.py record --task "design system" --model opus --agent architect --outcome success
    python router_learning.py record --task "complex refactor" --model sonnet --agent coder --outcome fail

    # Get recommendation based on learned patterns
    python router_learning.py recommend "task description"

    # Show stats
    python router_learning.py stats
    python router_learning.py stats --model opus
    python router_learning.py stats --agent architect
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Storage location
LEARNING_DB = Path.home() / ".claude" / "data" / "router_learning.json"

def ensure_db():
    """Ensure the learning database exists."""
    LEARNING_DB.parent.mkdir(parents=True, exist_ok=True)
    if not LEARNING_DB.exists():
        LEARNING_DB.write_text(json.dumps({
            "version": 1,
            "records": [],
            "aggregates": {
                "model_success": {},
                "agent_success": {},
                "pattern_success": {}
            }
        }, indent=2))

def load_db() -> dict:
    """Load the learning database."""
    ensure_db()
    return json.loads(LEARNING_DB.read_text())

def save_db(db: dict):
    """Save the learning database."""
    LEARNING_DB.write_text(json.dumps(db, indent=2))

def extract_patterns(task: str) -> list:
    """Extract keyword patterns from task description."""
    task_lower = task.lower()
    patterns = []

    # Task type patterns
    task_types = {
        'bug_fix': ['fix', 'bug', 'error', 'issue', 'broken', 'crash'],
        'feature': ['add', 'create', 'implement', 'build', 'new'],
        'refactor': ['refactor', 'reorganize', 'restructure', 'clean up'],
        'architecture': ['design', 'architect', 'plan', 'system', 'infrastructure'],
        'research': ['analyze', 'investigate', 'understand', 'explore', 'find'],
        'testing': ['test', 'spec', 'coverage', 'e2e', 'unit'],
        'docs': ['document', 'readme', 'comment', 'explain'],
        'security': ['security', 'audit', 'vulnerability', 'auth'],
        'performance': ['optimize', 'performance', 'speed', 'slow', 'memory'],
        'ui': ['ui', 'frontend', 'component', 'style', 'css', 'tailwind'],
    }

    for pattern_name, keywords in task_types.items():
        if any(kw in task_lower for kw in keywords):
            patterns.append(pattern_name)

    # Complexity indicators
    complexity_high = ['complex', 'entire', 'all', 'system', 'massive', 'full']
    complexity_low = ['simple', 'small', 'minor', 'quick', 'typo', 'single']

    if any(c in task_lower for c in complexity_high):
        patterns.append('complexity_high')
    elif any(c in task_lower for c in complexity_low):
        patterns.append('complexity_low')
    else:
        patterns.append('complexity_medium')

    return patterns if patterns else ['general']

def record_outcome(task: str, model: str, agent: str, outcome: str):
    """Record a routing decision outcome."""
    db = load_db()

    patterns = extract_patterns(task)

    record = {
        "timestamp": datetime.now().isoformat(),
        "task": task[:200],  # Truncate long tasks
        "model": model,
        "agent": agent,
        "outcome": outcome,  # success, fail, partial
        "patterns": patterns
    }

    db["records"].append(record)

    # Update aggregates
    agg = db["aggregates"]

    # Model success rates
    if model not in agg["model_success"]:
        agg["model_success"][model] = {"success": 0, "fail": 0, "partial": 0}
    agg["model_success"][model][outcome] = agg["model_success"][model].get(outcome, 0) + 1

    # Agent success rates
    if agent not in agg["agent_success"]:
        agg["agent_success"][agent] = {"success": 0, "fail": 0, "partial": 0}
    agg["agent_success"][agent][outcome] = agg["agent_success"][agent].get(outcome, 0) + 1

    # Pattern success rates (model+pattern combo)
    for pattern in patterns:
        key = f"{model}:{pattern}"
        if key not in agg["pattern_success"]:
            agg["pattern_success"][key] = {"success": 0, "fail": 0, "partial": 0}
        agg["pattern_success"][key][outcome] = agg["pattern_success"][key].get(outcome, 0) + 1

    save_db(db)

    total = len(db["records"])
    print(f"Recorded: {outcome} for {model}/{agent}")
    print(f"Total records: {total}")

def calculate_success_rate(stats: dict) -> float:
    """Calculate success rate from stats dict."""
    total = stats.get("success", 0) + stats.get("fail", 0) + stats.get("partial", 0)
    if total == 0:
        return 0.5  # Default neutral score
    # Partial counts as 0.5 success
    score = stats.get("success", 0) + (stats.get("partial", 0) * 0.5)
    return score / total

def get_recommendation(task: str) -> dict:
    """Get routing recommendation based on learned patterns."""
    import importlib.util
    db = load_db()
    agg = db["aggregates"]
    patterns = extract_patterns(task)

    # Base scores from smart_router logic (dynamic import from same directory)
    smart_router_path = Path(__file__).parent / "smart_router.py"
    spec = importlib.util.spec_from_file_location("smart_router", smart_router_path)
    smart_router = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(smart_router)
    base = smart_router.analyze_task(task)

    # Calculate learned adjustments
    model_scores = {}
    for model in ["sonnet", "opus", "gemini-2.5-flash", "glm-4.7", "haiku"]:
        score = 0.5  # Base neutral
        count = 0

        # Model overall success
        if model in agg["model_success"]:
            model_rate = calculate_success_rate(agg["model_success"][model])
            score += model_rate * 0.3
            count += 1

        # Pattern-specific success for this model
        for pattern in patterns:
            key = f"{model}:{pattern}"
            if key in agg["pattern_success"]:
                pattern_rate = calculate_success_rate(agg["pattern_success"][key])
                score += pattern_rate * 0.4
                count += 1

        if count > 0:
            model_scores[model] = score / count
        else:
            model_scores[model] = 0.5

    # Combine base recommendation with learned scores
    learned_best = max(model_scores.keys(), key=lambda k: model_scores[k])
    learned_score = model_scores[learned_best]

    result = {
        "base_model": base["model"],
        "base_confidence": base["confidence"],
        "learned_model": learned_best,
        "learned_score": round(learned_score, 2),
        "patterns_detected": patterns,
        "recommendation": base["model"],  # Default to base
        "source": "base"
    }

    # Override if learned data strongly suggests different model
    # Require at least 5 data points and >70% success rate difference
    total_records = len(db["records"])
    if total_records >= 5 and learned_score > 0.7 and learned_best != base["model"]:
        # Check if learned model has significantly better track record for these patterns
        base_score = model_scores.get(base["model"], 0.5)
        if learned_score - base_score > 0.15:
            result["recommendation"] = learned_best
            result["source"] = "learned"
            result["override_reason"] = f"Learned: {learned_best} has {learned_score:.0%} success vs {base_score:.0%} for {base['model']}"

    return result

def show_stats(model: str | None = None, agent: str | None = None):
    """Show learning statistics."""
    db = load_db()
    agg = db["aggregates"]

    print(f"\n=== Router Learning Stats ===")
    print(f"Total records: {len(db['records'])}")
    print()

    if model:
        # Show specific model stats
        if model in agg["model_success"]:
            stats = agg["model_success"][model]
            rate = calculate_success_rate(stats)
            print(f"Model: {model}")
            print(f"  Success: {stats.get('success', 0)}")
            print(f"  Fail: {stats.get('fail', 0)}")
            print(f"  Partial: {stats.get('partial', 0)}")
            print(f"  Success Rate: {rate:.0%}")
        else:
            print(f"No data for model: {model}")
    elif agent:
        # Show specific agent stats
        if agent in agg["agent_success"]:
            stats = agg["agent_success"][agent]
            rate = calculate_success_rate(stats)
            print(f"Agent: {agent}")
            print(f"  Success: {stats.get('success', 0)}")
            print(f"  Fail: {stats.get('fail', 0)}")
            print(f"  Partial: {stats.get('partial', 0)}")
            print(f"  Success Rate: {rate:.0%}")
        else:
            print(f"No data for agent: {agent}")
    else:
        # Show all stats
        print("Model Success Rates:")
        for m, stats in sorted(agg["model_success"].items()):
            rate = calculate_success_rate(stats)
            total = stats.get('success', 0) + stats.get('fail', 0) + stats.get('partial', 0)
            print(f"  {m}: {rate:.0%} ({total} tasks)")

        print("\nAgent Success Rates:")
        for a, stats in sorted(agg["agent_success"].items()):
            rate = calculate_success_rate(stats)
            total = stats.get('success', 0) + stats.get('fail', 0) + stats.get('partial', 0)
            print(f"  {a}: {rate:.0%} ({total} tasks)")

        print("\nTop Pattern Combinations:")
        pattern_rates = []
        for key, stats in agg["pattern_success"].items():
            rate = calculate_success_rate(stats)
            total = stats.get('success', 0) + stats.get('fail', 0) + stats.get('partial', 0)
            if total >= 2:  # Only show patterns with enough data
                pattern_rates.append((key, rate, total))

        for key, rate, total in sorted(pattern_rates, key=lambda x: -x[1])[:10]:
            print(f"  {key}: {rate:.0%} ({total} tasks)")

def main():
    parser = argparse.ArgumentParser(description="Router Learning System")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Record command
    record_parser = subparsers.add_parser("record", help="Record a routing outcome")
    record_parser.add_argument("--task", "-t", required=True, help="Task description")
    record_parser.add_argument("--model", "-m", required=True, help="Model used")
    record_parser.add_argument("--agent", "-a", required=True, help="Agent used")
    record_parser.add_argument("--outcome", "-o", required=True,
                               choices=["success", "fail", "partial"],
                               help="Outcome of the task")

    # Recommend command
    rec_parser = subparsers.add_parser("recommend", help="Get recommendation for a task")
    rec_parser.add_argument("task", help="Task description")
    rec_parser.add_argument("--json", action="store_true", help="JSON output")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show learning statistics")
    stats_parser.add_argument("--model", "-m", help="Filter by model")
    stats_parser.add_argument("--agent", "-a", help="Filter by agent")

    args = parser.parse_args()

    if args.command == "record":
        record_outcome(args.task, args.model, args.agent, args.outcome)
    elif args.command == "recommend":
        result = get_recommendation(args.task)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\nTask: {args.task[:60]}...")
            print(f"Patterns: {', '.join(result['patterns_detected'])}")
            print(f"Base recommendation: {result['base_model']} ({result['base_confidence']:.0%})")
            print(f"Learned best: {result['learned_model']} ({result['learned_score']:.0%})")
            print(f"\nFinal: {result['recommendation']} (source: {result['source']})")
            if result.get('override_reason'):
                print(f"Override: {result['override_reason']}")
    elif args.command == "stats":
        show_stats(args.model, args.agent)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
