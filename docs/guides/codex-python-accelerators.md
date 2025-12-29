# 10 Codex tricks that make Python development 3× faster

Codex (and Copilot’s Codex engine) can serve as an on-demand senior developer when you frame the right prompts. These ten workflows pair the article’s insights with concrete, copy-ready commands for Codex sessions.

---

## 1. Prompt-driven architecture

- **Use when**: You need scaffolding for APIs, CLIs, data pipelines, or background workers.
- **How to ask Codex**:
  ```
  Generate FastAPI scaffolding for creating a user:
  - Async endpoint at POST /users
  - Email validation with pydantic model
  - Insert into async SQLAlchemy session
  - Return created user with 201 status
  ```
- **Bonus**: Keep acceptance criteria in bullet form; Codex translates them into structure without you writing boilerplate.

---

## 2. Live refactoring partner

- **Use when**: Code feels verbose or non-pythonic.
- **Prompt**:
  ```
  Refactor this snippet to the most pythonic form. Explain why each change is safer or faster.
  ```
- **Tip**: Paste the code block first. Codex will suggest comprehensions, context managers, or itertools patterns and justify the improvements.

---

## 3. High-quality docstrings

- **Use when**: Functions lack documentation.
- **Prompt**:
  ```
  Add concise Google-style docstrings to these functions. Highlight args, returns, and side effects.
  ```
- **Automation**: Run across a module (`select code → ask Codex`) to build doc coverage quickly.

---

## 4. Regex without the browser tab

- **Use when**: You need a pattern and validation helpers.
- **Prompt**:
  ```
  Write a Python regex that extracts all email addresses from text. Provide re.findall usage and a validation helper.
  ```
- **Result**: Codex outputs both the pattern and usage snippet, saving the trip to regex sites.

---

## 5. Pseudocode → production code

- **Workflow**:
  1. Outline the algorithm in plain steps.
  2. Ask Codex to translate it.
  ```
  Convert this pseudocode into idiomatic pandas code:
  - Read sales.csv
  - Filter rows with sales > 1000
  - Group by region and sum revenue
  - Sort descending and return DataFrame
  ```
- **Outcome**: Clean pandas pipelines that mirror the written plan.

---

## 6. Test scaffolding in seconds

- **Prompt**:
  ```
  Create pytest unit tests for calculate_tax(price, rate). Cover happy path, zero price, negative rate.
  ```
- **Add-on**: Request parameterized fixtures or hypothesis strategies for broader coverage.

---

## 7. Comment legacy code automatically

- **Prompt**:
  ```
  Add inline comments explaining each step of this function. Focus on intent and side effects.
  ```
- **Use for**: Rapid onboarding to unfamiliar modules and clarifying cryptic loops.

---

## 8. One-liner simplification

- **Prompt**:
  ```
  Rewrite this logic as the most readable one-liner. Explain the trade-offs.
  ```
- **Result**: Concise list/set/dict comprehensions with rationale if readability might suffer.

---

## 9. Security-aware suggestions

- **Prompt**:
  ```
  Review this SQL query for security issues. Suggest parameterized updates and input validation.
  ```
- **Bonus**: Ask for pydantic models or dataclasses to enforce schema validation.

---

## 10. Discover better libraries

- **Prompt**:
  ```
  Recommend Python libraries for detecting language in text. Provide usage examples.
  ```
- **Outcome**: Codex surfaces lesser-known packages with quick-start code, expanding your toolbox.

---

### Quick deployment inside Codex sessions

Copy any prompt into Codex after launching via `scx`. The startup command loads `.codex-config.md`, so the assistant already knows your tools (`tools/ai-collaboration/change-tracker.py`, `docs/guides/codex-layered-mastery.md`, etc.) and tone. Use the prompts as-is or adapt them into multi-step Codex blocks for repeatable workflows. Copy instructions sit in `prompts/python-accelerators.txt` for one-line sharing.
