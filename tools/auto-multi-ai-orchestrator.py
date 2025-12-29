#!/usr/bin/env python3
"""
Automated Multi-AI Orchestrator
Calls Codex CLI and Gemini API automatically - no manual steps

Based on Codex GPT-5 & Gemini 2.0 Feedback (2025-10-14):
- Automated CLI/API calls (no manual copy-paste)
- Secure secret storage (environment variables, not hardcoded)
- Input sanitization to prevent command injection
- Proper exit code parsing and stderr capture
- Structured logging with audit trails
- Circuit breaker pattern for reliability
- Request-level quotas and monitoring

Usage:
    python auto-multi-ai-orchestrator.py --task "Your task" --code "optional code to review"

    Environment Variables:
    - GOOGLE_API_KEY: Gemini API key (or use --google-api-key)
    - CODEX_CLI_PATH: Custom path to Codex CLI (optional)
"""

import argparse
import json
import subprocess
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import os
import hashlib

try:
    import google.generativeai as genai
except ImportError:
    print("ERROR: google-generativeai not installed")
    print("Install with: pip install google-generativeai")
    sys.exit(1)

# ============================================================================
# Configuration
# ============================================================================

LOG_DIR = Path("logs/multi-ai")
LOG_DIR.mkdir(parents=True, exist_ok=True)

HIGH_RISK_PATTERNS = [
    "security", "auth", "authentication", "authorization",
    "oauth", "jwt", "password", "credential", "token",
    "production", "database migration", "payment"
]

# Circuit Breaker Configuration
CIRCUIT_BREAKER_THRESHOLD = 3  # Failures before opening circuit
CIRCUIT_BREAKER_TIMEOUT = 60  # Seconds to wait before retry
CIRCUIT_BREAKER_STATE = {
    "codex": {"failures": 0, "state": "closed", "last_failure": None},
    "gemini": {"failures": 0, "state": "closed", "last_failure": None}
}

# Input Sanitization Patterns (prevent command injection)
# Note: Parentheses removed from dangerous patterns - they're legitimate in task descriptions
# Only blocking truly dangerous shell metacharacters
DANGEROUS_PATTERNS = [
    r'[;&|`$]',  # Shell metacharacters (removed parentheses)
    r'\\x[0-9a-fA-F]{2}',  # Hex escapes
    r'\x00',  # Null bytes
]

# ============================================================================
# Input Sanitization
# ============================================================================

def sanitize_input(text: str, max_length: int = 50000) -> str:
    """
    Sanitize user input to prevent command injection and other attacks

    Based on Codex GPT-5 recommendation:
    "sanitize input before passing user text to CLI to block command injection"
    """
    if not text:
        return ""

    # Limit length to prevent resource exhaustion
    if len(text) > max_length:
        text = text[:max_length]

    # Check for dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, text):
            raise ValueError(f"Input contains potentially dangerous pattern: {pattern}")

    # Remove null bytes
    text = text.replace('\x00', '')

    return text

def hash_for_audit(text: str) -> str:
    """Create hash for audit trail without storing sensitive content"""
    return hashlib.sha256(text.encode()).hexdigest()[:16]

# ============================================================================
# Logging
# ============================================================================

class OrchestrationLogger:
    """
    Structured logging for audit trail

    Based on Codex GPT-5 recommendation:
    "Implement request-level quotas, exponential backoff, and audit trails"
    """

    def __init__(self, task: str):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = LOG_DIR / f"session_{self.session_id}.json"
        self.log = {
            "session_id": self.session_id,
            "task": task,
            "task_hash": hash_for_audit(task),  # For audit without exposing content
            "start_time": datetime.now().isoformat(),
            "events": [],
            "codex_response": None,
            "gemini_response": None,
            "errors": [],
            "security": {
                "input_sanitized": False,
                "dangerous_patterns_detected": []
            }
        }

    def log_event(self, event_type: str, data: Any):
        """Log an event"""
        self.log["events"].append({
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        })
        self._save()

    def log_error(self, error: str, agent: str = None):
        """Log an error"""
        self.log["errors"].append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "error": error
        })
        self._save()

    def set_codex_response(self, response: Dict[str, Any]):
        """Store Codex response"""
        self.log["codex_response"] = response
        self._save()

    def set_gemini_response(self, response: Dict[str, Any]):
        """Store Gemini response"""
        self.log["gemini_response"] = response
        self._save()

    def finalize(self):
        """Finalize the log"""
        self.log["end_time"] = datetime.now().isoformat()
        self._save()
        print(f"\n[LOG] Session log saved: {self.log_file}")

    def _save(self):
        """Save log to disk"""
        with open(self.log_file, 'w') as f:
            json.dump(self.log, f, indent=2)

# ============================================================================
# Circuit Breaker
# ============================================================================

def check_circuit_breaker(agent: str) -> bool:
    """
    Check if circuit breaker is open for agent

    Based on Gemini recommendation:
    "Use the circuit breaker pattern to prevent cascading failures"
    """
    state = CIRCUIT_BREAKER_STATE[agent]

    if state["state"] == "open":
        # Check if timeout has elapsed
        if state["last_failure"]:
            elapsed = time.time() - state["last_failure"]
            if elapsed >= CIRCUIT_BREAKER_TIMEOUT:
                print(f"[{agent.upper()}] Circuit breaker timeout elapsed, resetting to half-open")
                state["state"] = "half-open"
                state["failures"] = 0
                return True
            else:
                print(f"[{agent.upper()}] Circuit breaker OPEN (wait {CIRCUIT_BREAKER_TIMEOUT - elapsed:.0f}s)")
                return False

    return True

def record_failure(agent: str):
    """Record failure and potentially open circuit breaker"""
    state = CIRCUIT_BREAKER_STATE[agent]
    state["failures"] += 1
    state["last_failure"] = time.time()

    if state["failures"] >= CIRCUIT_BREAKER_THRESHOLD:
        state["state"] = "open"
        print(f"[{agent.upper()}] Circuit breaker OPENED after {state['failures']} failures")

def record_success(agent: str):
    """Record success and close circuit breaker"""
    state = CIRCUIT_BREAKER_STATE[agent]
    if state["state"] == "half-open":
        state["state"] = "closed"
        print(f"[{agent.upper()}] Circuit breaker CLOSED")
    state["failures"] = 0

# ============================================================================
# Codex Integration (CLI)
# ============================================================================

def call_codex_cli(prompt: str, logger: OrchestrationLogger, max_retries: int = 2) -> Dict[str, Any]:
    """
    Call Codex CLI with retries, error handling, and circuit breaker

    Based on Codex GPT-5 recommendations:
    - Input sanitization
    - Exit code parsing
    - Stderr capture
    - Circuit breaker pattern

    Returns:
        Dict with 'success', 'response', 'error' keys
    """
    # Check circuit breaker
    if not check_circuit_breaker("codex"):
        error = "Codex circuit breaker is OPEN"
        logger.log_error(error, "codex")
        return {
            "success": False,
            "error": error,
            "agent": "codex"
        }

    # Sanitize input (but allow legitimate syntax in tasks and code)
    # Only block truly dangerous patterns like command injection attempts
    try:
        # Always sanitize, but dangerous patterns exclude parentheses now
        # Parentheses are legitimate in: function calls, conditionals, tuples, etc.
        prompt = sanitize_input(prompt)
        logger.log["security"]["input_sanitized"] = True
    except ValueError as e:
        error = f"Input sanitization failed: {str(e)}"
        logger.log_error(error, "codex")
        logger.log["security"]["dangerous_patterns_detected"].append(str(e))
        return {
            "success": False,
            "error": error,
            "agent": "codex"
        }

    logger.log_event("codex_call_start", {
        "prompt_length": len(prompt),
        "prompt_hash": hash_for_audit(prompt)
    })

    # Try to find Codex CLI
    codex_paths = [
        'codex',  # If in PATH
        'C:\\Users\\SainathreddyDadiredd\\AppData\\Roaming\\npm\\codex.cmd',  # Windows npm with .cmd
    ]

    codex_cmd = None
    for path in codex_paths:
        try:
            subprocess.run([path, '--version'], capture_output=True, timeout=5, shell=True)
            codex_cmd = path
            print(f"[CODEX] Found Codex at: {path}")
            break
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue

    if not codex_cmd:
        error = "Codex CLI not found in any expected location. Install: npm install -g @openai/codex"
        print(f"[CODEX] ERROR: {error}")
        logger.log_error(error, "codex")
        return {
            "success": False,
            "error": error,
            "agent": "codex"
        }

    for attempt in range(max_retries):
        try:
            print(f"\n[CODEX] Calling Codex CLI (attempt {attempt + 1}/{max_retries})...")

            # Use stdin to pass prompt (with UTF-8 encoding for Windows)
            result = subprocess.run(
                [codex_cmd, 'exec', '--full-auto'],
                input=prompt,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',  # Replace invalid chars instead of crashing
                timeout=60,
                shell=True
            )

            # Check exit code (Codex GPT-5: "parse exit codes and capture stderr")
            if result.returncode != 0:
                error_msg = f"Codex CLI exited with code {result.returncode}"
                if result.stderr:
                    error_msg += f": {result.stderr[:200]}"
                raise Exception(error_msg)

            # Codex outputs a lot of metadata, extract just the response
            output = result.stdout if result.stdout else ""
            error_output = result.stderr if result.stderr else ""

            # Log raw output for debugging
            print(f"[CODEX DEBUG] stdout length: {len(output)}, exit code: {result.returncode}")

            if not output:
                raise Exception(f"Empty stdout from Codex. stderr: {error_output[:200]}")

            output = output.strip()

            # Codex CLI output format:
            # 1. Welcome messages
            # 2. "Reading prompt from stdin..."
            # 3. Configuration block between "--------"
            # 4. "user" section with prompt
            # 5. "thinking" section
            # 6. "codex" section with actual response (THIS IS WHAT WE WANT)
            # 7. "tokens used" section

            # Codex has TWO output formats:
            # 1. Interactive (with markers): ...\ncodex\n<response>\ntokens used\n...
            # 2. Subprocess/piped: Just the raw response

            codex_marker = '\ncodex\n'
            tokens_marker = '\ntokens used\n'

            response = ""

            if codex_marker in output and tokens_marker in output:
                # Format 1: Interactive with markers
                start_idx = output.find(codex_marker) + len(codex_marker)
                end_idx = output.find(tokens_marker, start_idx)

                if end_idx > start_idx:
                    response = output[start_idx:end_idx].strip()
                else:
                    response = output[start_idx:].strip()
            else:
                # Format 2: Subprocess/piped - entire output IS the response
                response = output.strip()

            # Clean up any remaining markers or metadata
            if '\ntokens used\n' in response:
                response = response[:response.find('\ntokens used')].strip()

            # Remove welcome messages that sometimes appear
            unwanted_prefixes = [
                "Hey! I'm ready",
                "Hey there",
                "Everything's set up",
                "I'm ready whenever"
            ]
            for unwanted in unwanted_prefixes:
                if response.startswith(unwanted):
                    # This is just a welcome message, not an actual analysis
                    # Try to find actual content after it
                    lines = response.split('\n')
                    if len(lines) > 1:
                        response = '\n'.join(lines[1:]).strip()
                    break

            if response:
                logger.log_event("codex_call_success", {
                    "response_length": len(response),
                    "response_hash": hash_for_audit(response),
                    "exit_code": result.returncode
                })
                logger.set_codex_response({
                    "success": True,
                    "response": response,
                    "attempt": attempt + 1
                })

                # Record success for circuit breaker
                record_success("codex")

                print(f"[CODEX] Success! Got {len(response)} chars response")
                return {
                    "success": True,
                    "response": response,
                    "agent": "codex"
                }
            else:
                raise Exception("Empty response from Codex")

        except subprocess.TimeoutExpired:
            error = f"Codex timeout on attempt {attempt + 1}"
            print(f"[CODEX] {error}")
            logger.log_error(error, "codex")
            record_failure("codex")

            if attempt < max_retries - 1:
                print(f"[CODEX] Retrying in 2 seconds...")
                time.sleep(2)

        except FileNotFoundError:
            error = f"Codex CLI command failed: {codex_cmd}"
            print(f"[CODEX] ERROR: {error}")
            logger.log_error(error, "codex")
            record_failure("codex")

            if attempt < max_retries - 1:
                print(f"[CODEX] Retrying in 2 seconds...")
                time.sleep(2)

        except Exception as e:
            error = f"Codex error: {str(e)}"
            print(f"[CODEX] ERROR: {error}")
            logger.log_error(error, "codex")
            record_failure("codex")

            if attempt < max_retries - 1:
                print(f"[CODEX] Retrying in 2 seconds...")
                time.sleep(2)

    # All retries failed
    error = f"Codex failed after {max_retries} attempts"
    logger.log_error(error, "codex")
    record_failure("codex")
    return {
        "success": False,
        "error": error,
        "agent": "codex"
    }

# ============================================================================
# Gemini Integration (API)
# ============================================================================

def call_gemini_api(prompt: str, logger: OrchestrationLogger, max_retries: int = 2) -> Dict[str, Any]:
    """
    Call Gemini API with retries, error handling, and circuit breaker

    Based on Codex GPT-5 & Gemini recommendations:
    - Input sanitization
    - Circuit breaker pattern
    - TLS verification (handled by Google API)
    - Structured logging

    Returns:
        Dict with 'success', 'response', 'error' keys
    """
    # Check circuit breaker
    if not check_circuit_breaker("gemini"):
        error = "Gemini circuit breaker is OPEN"
        logger.log_error(error, "gemini")
        return {
            "success": False,
            "error": error,
            "agent": "gemini"
        }

    # Sanitize input (but allow legitimate syntax in tasks and code)
    # Only block truly dangerous patterns like command injection attempts
    try:
        # Always sanitize, but dangerous patterns exclude parentheses now
        # Parentheses are legitimate in: function calls, conditionals, tuples, etc.
        prompt = sanitize_input(prompt)
        logger.log["security"]["input_sanitized"] = True
    except ValueError as e:
        error = f"Input sanitization failed: {str(e)}"
        logger.log_error(error, "gemini")
        logger.log["security"]["dangerous_patterns_detected"].append(str(e))
        return {
            "success": False,
            "error": error,
            "agent": "gemini"
        }

    logger.log_event("gemini_call_start", {
        "prompt_length": len(prompt),
        "prompt_hash": hash_for_audit(prompt)
    })

    # Check for API key (Codex GPT-5: "Require secure secret storage")
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        error = "GOOGLE_API_KEY not set. Use environment variable or --google-api-key parameter"
        print(f"[GEMINI] ERROR: {error}")
        logger.log_error(error, "gemini")
        record_failure("gemini")
        return {
            "success": False,
            "error": error,
            "agent": "gemini"
        }

    genai.configure(api_key=api_key)

    for attempt in range(max_retries):
        try:
            print(f"\n[GEMINI] Calling Gemini API (attempt {attempt + 1}/{max_retries})...")

            # Use gemini-2.0-flash-exp (free tier)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            response = model.generate_content(prompt)

            if response.text:
                logger.log_event("gemini_call_success", {
                    "response_length": len(response.text),
                    "response_hash": hash_for_audit(response.text)
                })
                logger.set_gemini_response({
                    "success": True,
                    "response": response.text,
                    "attempt": attempt + 1
                })

                # Record success for circuit breaker
                record_success("gemini")

                print(f"[GEMINI] Success! Got {len(response.text)} chars response (FREE!)")
                return {
                    "success": True,
                    "response": response.text,
                    "agent": "gemini",
                    "cost": 0.0  # FREE!
                }
            else:
                raise Exception("Empty response from Gemini")

        except Exception as e:
            error = f"Gemini error: {str(e)}"
            print(f"[GEMINI] ERROR: {error}")
            logger.log_error(error, "gemini")
            record_failure("gemini")

            if attempt < max_retries - 1:
                # Exponential backoff (Gemini recommendation)
                wait_time = 2 ** attempt
                print(f"[GEMINI] Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    # All retries failed
    error = f"Gemini failed after {max_retries} attempts"
    logger.log_error(error, "gemini")
    record_failure("gemini")
    return {
        "success": False,
        "error": error,
        "agent": "gemini"
    }

# ============================================================================
# Orchestration Logic
# ============================================================================

def orchestrate_multi_ai(
    task: str,
    code: Optional[str] = None,
    force_validation: bool = False,
    force_research: bool = False
) -> Dict[str, Any]:
    """
    Main orchestration function

    Args:
        task: The task description
        code: Optional code to validate
        force_validation: Force Codex validation
        force_research: Force Gemini research

    Returns:
        Dict with orchestration results
    """

    logger = OrchestrationLogger(task)

    print("=" * 70)
    print("AUTOMATED MULTI-AI ORCHESTRATOR")
    print("=" * 70)
    print(f"Task: {task[:60]}{'...' if len(task) > 60 else ''}")
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Determine if validation/research needed
    is_high_risk = any(pattern in task.lower() for pattern in HIGH_RISK_PATTERNS)
    needs_validation = force_validation or is_high_risk or code is not None
    needs_research = force_research or "best practice" in task.lower() or "how" in task.lower()

    print(f"\n[ANALYSIS]")
    print(f"  High-risk task: {is_high_risk}")
    print(f"  Needs Codex validation: {needs_validation}")
    print(f"  Needs Gemini research: {needs_research}")

    result = {
        "task": task,
        "start_time": datetime.now().isoformat(),
        "is_high_risk": is_high_risk,
        "codex": None,
        "gemini": None,
        "summary": None
    }

    # Step 1: Codex validation (if needed)
    if needs_validation:
        if code:
            codex_prompt = f"""Review this code for security vulnerabilities, edge cases, and best practices:

TASK: {task}

CODE:
{code}

Provide critical analysis focusing on:
1. Security vulnerabilities
2. Edge cases not handled
3. Performance concerns
4. Best practices violations

Be specific and actionable."""
        else:
            codex_prompt = f"""Analyze this task for potential issues and provide guidance:

TASK: {task}

Focus on:
1. Security considerations
2. Common pitfalls
3. Edge cases to handle
4. Critical best practices"""

        codex_result = call_codex_cli(codex_prompt, logger)
        result["codex"] = codex_result

    # Step 2: Gemini research (if needed)
    if needs_research:
        gemini_prompt = f"""Research the best practices for this task in 2025:

TASK: {task}

Provide:
1. Current industry best practices
2. Recommended approaches and patterns
3. Common pitfalls to avoid
4. Modern tools and libraries

Be specific and cite sources if possible."""

        gemini_result = call_gemini_api(gemini_prompt, logger)
        result["gemini"] = gemini_result

    # Step 3: Synthesize results
    print("\n" + "=" * 70)
    print("SYNTHESIS")
    print("=" * 70)

    summary = {
        "has_codex_feedback": result["codex"] is not None and result["codex"]["success"],
        "has_gemini_feedback": result["gemini"] is not None and result["gemini"]["success"],
        "critical_issues": [],
        "recommendations": [],
        "best_practices": []
    }

    if result["codex"] and result["codex"]["success"]:
        print("\n[CODEX FEEDBACK RECEIVED]")
        print(f"  Response: {len(result['codex']['response'])} chars")
        # Parse for critical keywords
        codex_text = result["codex"]["response"].lower()
        if "critical" in codex_text or "vulnerability" in codex_text:
            summary["critical_issues"].append("Codex identified critical security concerns")

    if result["gemini"] and result["gemini"]["success"]:
        print("\n[GEMINI FEEDBACK RECEIVED]")
        print(f"  Response: {len(result['gemini']['response'])} chars")
        print(f"  Cost: FREE!")

    result["summary"] = summary
    result["end_time"] = datetime.now().isoformat()

    logger.finalize()

    print("\n" + "=" * 70)
    print("ORCHESTRATION COMPLETE")
    print("=" * 70)

    return result

# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Automated Multi-AI Orchestrator - No manual steps!"
    )
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--code", help="Optional code to review")
    parser.add_argument("--validate", action="store_true", help="Force Codex validation")
    parser.add_argument("--research", action="store_true", help="Force Gemini research")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--google-api-key", help="Google API key for Gemini")

    args = parser.parse_args()

    # Set Google API key if provided
    if args.google_api_key:
        os.environ['GOOGLE_API_KEY'] = args.google_api_key

    # Run orchestration
    result = orchestrate_multi_ai(
        task=args.task,
        code=args.code,
        force_validation=args.validate,
        force_research=args.research
    )

    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n[OUTPUT] Saved to: {output_path}")

    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    if result["codex"] and result["codex"]["success"]:
        print("\n[CODEX ANALYSIS]")
        print(result["codex"]["response"][:500])
        if len(result["codex"]["response"]) > 500:
            print("... (truncated)")

    if result["gemini"] and result["gemini"]["success"]:
        print("\n[GEMINI RESEARCH]")
        print(result["gemini"]["response"][:500])
        if len(result["gemini"]["response"]) > 500:
            print("... (truncated)")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
