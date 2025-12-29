#!/usr/bin/env python3
"""
Multi-AI Orchestrator - Integrated with Claude Code
Claude orchestrates, calls Codex/Gemini for feedback, implements suggestions

Usage: Called by Claude Code during conversation
- Claude analyzes task
- Calls Codex for validation when needed
- Calls Gemini for research when needed
- Implements suggestions from both
- Reports back with full context
"""

import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

def call_codex_for_validation(task: str, code_to_validate: str, timeout: int = 45) -> Dict[str, Any]:
    """
    Call Codex CLI to validate code/approach

    Args:
        task: Original task description
        code_to_validate: Code or approach to validate
        timeout: Timeout in seconds

    Returns:
        Dict with validation results
    """
    prompt = f"""You are reviewing this implementation for potential issues:

TASK: {task}

IMPLEMENTATION:
{code_to_validate}

Please provide validation feedback focusing on:
1. Security vulnerabilities
2. Edge cases not handled
3. Performance concerns
4. Test coverage gaps

Respond in JSON format:
{{
  "verdict": "approve|revise",
  "confidence": 0.0-1.0,
  "issues": ["issue 1", "issue 2"],
  "suggestions": ["suggestion 1", "suggestion 2"],
  "critical_risks": ["risk 1"]
}}"""

    try:
        result = subprocess.run(
            ['codex', 'exec', '--full-auto'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = result.stdout.strip()

        # Try to parse JSON from output
        json_start = output.find('{')
        json_end = output.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = output[json_start:json_end]
            data = json.loads(json_str)
            return {
                "success": True,
                "agent": "codex",
                **data
            }
        else:
            # If no JSON, return raw output
            return {
                "success": True,
                "agent": "codex",
                "verdict": "approve" if "looks good" in output.lower() else "review_needed",
                "confidence": 0.75,
                "raw_response": output,
                "issues": [],
                "suggestions": [],
                "critical_risks": []
            }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Codex timeout after {timeout}s",
            "agent": "codex"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Codex CLI not found. Install: npm install -g @openai/codex",
            "agent": "codex"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent": "codex"
        }

def call_gemini_for_research(task: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Call Gemini CLI for research/suggestions

    Args:
        task: Research task or question
        timeout: Timeout in seconds

    Returns:
        Dict with research results
    """
    prompt = f"""Research task: {task}

Please provide:
1. Current best practices
2. Latest trends/patterns
3. Recommended approaches
4. Potential pitfalls to avoid

Respond in JSON format:
{{
  "confidence": 0.0-1.0,
  "best_practices": ["practice 1", "practice 2"],
  "recommendations": ["recommendation 1"],
  "pitfalls": ["pitfall 1"],
  "sources": ["source 1"]
}}"""

    try:
        result = subprocess.run(
            ['gemini', '-p', prompt, '-o', 'text'],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = result.stdout.strip()

        # Try to parse JSON from output
        json_start = output.find('{')
        json_end = output.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = output[json_start:json_end]
            data = json.loads(json_str)
            return {
                "success": True,
                "agent": "gemini",
                "cost": 0.0,  # FREE!
                **data
            }
        else:
            # If no JSON, return raw output
            return {
                "success": True,
                "agent": "gemini",
                "confidence": 0.70,
                "raw_response": output,
                "best_practices": [],
                "recommendations": [],
                "pitfalls": []
            }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Gemini timeout after {timeout}s",
            "agent": "gemini"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Gemini CLI not found. Install: npm install -g @google/gemini-cli",
            "agent": "gemini"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent": "gemini"
        }

def orchestrate_multi_ai_workflow(
    task: str,
    implementation: Optional[str] = None,
    needs_validation: bool = True,
    needs_research: bool = False
) -> Dict[str, Any]:
    """
    Orchestrate multi-AI workflow

    Claude (you) orchestrates, calls Codex/Gemini as needed

    Args:
        task: The task description
        implementation: Code/approach to validate (if any)
        needs_validation: Whether to call Codex for validation
        needs_research: Whether to call Gemini for research

    Returns:
        Dict with all AI feedback consolidated
    """
    result = {
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "claude_orchestrating": True,
        "feedback": {}
    }

    # Step 1: Research phase (if needed)
    if needs_research:
        print("\n[RESEARCH] Calling Gemini for research...")
        gemini_result = call_gemini_for_research(task)
        result["feedback"]["gemini"] = gemini_result

        if gemini_result.get("success"):
            print(f"[OK] Gemini research complete (FREE!)")
            if gemini_result.get("recommendations"):
                print(f"  Found {len(gemini_result['recommendations'])} recommendations")
        else:
            print(f"[WARNING] Gemini error: {gemini_result.get('error')}")

    # Step 2: Validation phase (if needed and have implementation)
    if needs_validation and implementation:
        print("\n[VALIDATION] Calling Codex for validation...")
        codex_result = call_codex_for_validation(task, implementation)
        result["feedback"]["codex"] = codex_result

        if codex_result.get("success"):
            verdict = codex_result.get("verdict", "unknown")
            print(f"[OK] Codex validation complete: {verdict.upper()}")

            issues = codex_result.get("issues", [])
            if issues:
                print(f"  Found {len(issues)} issues:")
                for issue in issues[:3]:
                    print(f"    - {issue}")

            suggestions = codex_result.get("suggestions", [])
            if suggestions:
                print(f"  Received {len(suggestions)} suggestions")
        else:
            print(f"[WARNING] Codex error: {codex_result.get('error')}")

    # Step 3: Synthesize feedback
    result["summary"] = synthesize_feedback(result["feedback"])

    return result

def synthesize_feedback(feedback: Dict[str, Any]) -> Dict[str, Any]:
    """Synthesize feedback from multiple AIs"""
    summary = {
        "needs_changes": False,
        "critical_issues": [],
        "suggestions": [],
        "best_practices": [],
        "confidence": 1.0
    }

    # Check Codex validation
    if "codex" in feedback:
        codex = feedback["codex"]
        if codex.get("success"):
            if codex.get("verdict") == "revise":
                summary["needs_changes"] = True

            summary["critical_issues"].extend(codex.get("critical_risks", []))
            summary["suggestions"].extend(codex.get("suggestions", []))
            summary["confidence"] = min(summary["confidence"], codex.get("confidence", 1.0))

    # Check Gemini research
    if "gemini" in feedback:
        gemini = feedback["gemini"]
        if gemini.get("success"):
            summary["best_practices"].extend(gemini.get("best_practices", []))
            summary["suggestions"].extend(gemini.get("recommendations", []))

    return summary

# ============================================================================
# Helper function for Claude to use
# ============================================================================

def get_multi_ai_feedback(task: str, code: str = None) -> str:
    """
    Simple function for Claude to call to get multi-AI feedback

    Args:
        task: Task description
        code: Optional code to validate

    Returns:
        Formatted feedback string
    """
    # Determine what's needed
    high_risk_patterns = ["security", "auth", "oauth", "jwt", "password", "production", "database"]
    needs_validation = any(pattern in task.lower() for pattern in high_risk_patterns) or code is not None
    needs_research = "how" in task.lower() or "best practice" in task.lower() or "explain" in task.lower()

    # Run orchestration
    result = orchestrate_multi_ai_workflow(
        task=task,
        implementation=code,
        needs_validation=needs_validation,
        needs_research=needs_research
    )

    # Format response
    output = ["\n" + "="*70]
    output.append("MULTI-AI FEEDBACK")
    output.append("="*70)

    summary = result["summary"]

    if summary["critical_issues"]:
        output.append("\n[CRITICAL ISSUES]:")
        for issue in summary["critical_issues"]:
            output.append(f"  - {issue}")

    if summary["suggestions"]:
        output.append("\n[SUGGESTIONS]:")
        for suggestion in summary["suggestions"][:5]:
            output.append(f"  - {suggestion}")

    if summary["best_practices"]:
        output.append("\n[BEST PRACTICES]:")
        for practice in summary["best_practices"][:5]:
            output.append(f"  - {practice}")

    output.append(f"\n[CONFIDENCE]: {summary['confidence']:.2f}")
    output.append(f"[NEEDS CHANGES]: {'YES' if summary['needs_changes'] else 'NO'}")

    output.append("\n" + "="*70)

    # Save full result
    output_dir = Path("results/multi-ai-feedback")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"feedback_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    output.append(f"[SAVED]: Full feedback saved to: {output_file}")
    output.append("="*70)

    return "\n".join(output)

# ============================================================================
# Main execution (for testing)
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Multi-AI Orchestrator - Get feedback from Codex/Gemini")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--code", help="Code to validate (optional)")
    parser.add_argument("--validate", action="store_true", help="Force validation with Codex")
    parser.add_argument("--research", action="store_true", help="Force research with Gemini")

    args = parser.parse_args()

    result = orchestrate_multi_ai_workflow(
        task=args.task,
        implementation=args.code,
        needs_validation=args.validate or args.code is not None,
        needs_research=args.research
    )

    print("\n" + "="*70)
    print("MULTI-AI ORCHESTRATION COMPLETE")
    print("="*70)
    print(json.dumps(result, indent=2, default=str))
