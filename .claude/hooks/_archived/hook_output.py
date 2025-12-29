"""
Hook Output Helper - Unified output to both terminal and Claude context.

Usage:
    from hook_output import HookOutput

    output = HookOutput()
    output.terminal("[SEARCH] Detected: coding task")        # User sees in terminal
    output.context("Complex task detected. Use bd.")   # Claude sees in context
    output.emit()                                       # Prints final JSON
"""

import json
import sys


class HookOutput:
    """Unified hook output that sends to both terminal and Claude context."""

    def __init__(self, hook_name: str = "Hook"):
        self.hook_name = hook_name
        self._terminal_messages = []
        self._context_messages = []
        self._modified_prompt = None
        self._decision = None
        self._reason = None

    def terminal(self, message: str):
        """Add message visible in terminal UI (user sees this)."""
        self._terminal_messages.append(message)
        return self

    def context(self, message: str):
        """Add context injected to Claude (Claude sees this)."""
        self._context_messages.append(message)
        return self

    def both(self, terminal_msg: str, context_msg: str = None):
        """Add message to both terminal and context."""
        self._terminal_messages.append(terminal_msg)
        self._context_messages.append(context_msg or terminal_msg)
        return self

    def modify_prompt(self, new_prompt: str):
        """Replace the user's prompt (both see)."""
        self._modified_prompt = new_prompt
        return self

    def block(self, reason: str):
        """Block the prompt with a reason."""
        self._decision = "block"
        self._reason = reason
        self._terminal_messages.append(f"[STOP] {reason}")
        return self

    def emit(self):
        """Print the final JSON output and exit."""
        output = {}

        # Terminal message (user visible)
        if self._terminal_messages:
            output["systemMessage"] = " | ".join(self._terminal_messages)

        # Claude context (Claude visible)
        if self._context_messages or self._modified_prompt:
            hook_output = {"hookEventName": self.hook_name}

            if self._context_messages:
                hook_output["additionalContext"] = "\n".join(self._context_messages)

            if self._modified_prompt:
                hook_output["modifiedPrompt"] = self._modified_prompt

            output["hookSpecificOutput"] = hook_output

        # Block decision
        if self._decision:
            output["decision"] = self._decision
            output["reason"] = self._reason

        if output:
            print(json.dumps(output))

        sys.exit(0)

    def log_stderr(self, message: str):
        """Log to stderr (visible in terminal during execution)."""
        print(f"[{self.hook_name}] {message}", file=sys.stderr)
        return self


# Convenience function for simple cases
def emit_both(terminal_msg: str, context_msg: str = None, hook_name: str = "Hook"):
    """Quick helper to emit to both channels."""
    output = HookOutput(hook_name)
    output.terminal(terminal_msg)
    output.context(context_msg or terminal_msg)
    output.emit()
