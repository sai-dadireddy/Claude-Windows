"""
Generate an instruction index for Codex sessions.

The script scans key instruction directories (config files, global instructions,
Claude/Codex workspaces, MCP configs, tool references) and produces a concise
Markdown catalog so Codex can load context with a single file read.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / ".ai-workspace" / "codex" / "INSTRUCTION-INDEX.md"


def iter_files(base: Path, patterns: Iterable[str]) -> Iterable[Path]:
    for pattern in patterns:
        for path in base.glob(pattern):
            if path.is_file():
                if path.name.lower() == "active-style.md":
                    continue
                yield path


def first_meaningful_line(path: Path, limit: int = 140) -> str:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if stripped:
                    clean = unicodedata.normalize("NFKD", stripped)
                    clean = clean.replace("—", "-").replace("–", "-").replace("•", "-")
                    clean = clean.encode("ascii", "ignore").decode("ascii")
                    clean = "".join(ch for ch in clean if 32 <= ord(ch) < 127)
                    return (clean[: limit - 3] + "...") if len(clean) > limit else clean
    except Exception:
        return ""
    return ""


def describe_files(title: str, files: Iterable[Path], base: Path) -> str:
    lines: List[str] = [f"### {title}", ""]
    for path in sorted(files):
        rel = path.relative_to(base)
        summary = first_meaningful_line(path)
        summary_part = f" - {summary}" if summary else ""
        lines.append(f"- `{rel.as_posix()}`{summary_part}")
    lines.append("")
    return "\n".join(lines)


def load_mcp_entries(config_path: Path) -> List[Tuple[str, str]]:
    if not config_path.exists():
        return []
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    entries: List[Tuple[str, str]] = []
    servers = data.get("servers") or data
    if isinstance(servers, dict):
        for name, details in servers.items():
            command = ""
            if isinstance(details, dict):
                cmd = details.get("command") or ""
                args = details.get("args") or []
                if cmd:
                    command = cmd + (" " + " ".join(map(str, args)) if args else "")
            entries.append((name, command))
    return entries


def main() -> None:
    sections: List[str] = []

    sections.append("# Codex Instruction Index\n")
    sections.append("Generated automatically to gather all key instructions, MCP configs, and tool references Codex should load on startup.\n")

    # Core config files
    core_files = [
        REPO_ROOT / ".codex-config.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / ".claude-project.md",
        REPO_ROOT / ".clauderc",
    ]
    sections.append(describe_files("Core configuration", [p for p in core_files if p.exists()], REPO_ROOT))

    # Codex workspace docs
    codex_workspace = REPO_ROOT / ".ai-workspace" / "codex"
    sections.append(describe_files("Codex workspace docs", iter_files(codex_workspace, ["*.md"]), REPO_ROOT))

    # Global instructions
    global_instr_dir = REPO_ROOT / "global-instructions"
    sections.append(describe_files("Global instruction modules", iter_files(global_instr_dir, ["*.md"]), REPO_ROOT))

    # Claude command library
    claude_dir = REPO_ROOT / ".claude"
    if claude_dir.exists():
        sections.append(describe_files("Claude slash commands", iter_files(claude_dir / "commands", ["*.md"]), REPO_ROOT))
        sections.append(describe_files("Claude agents", iter_files(claude_dir / "agents", ["*.md"]), REPO_ROOT))

    # Docs + guides
    docs_dir = REPO_ROOT / "docs"
    sections.append(describe_files("Documentation (guides & quick references)", iter_files(docs_dir, ["guides/**/*.md", "quick-reference/**/*.md"]), REPO_ROOT))

    # Tools
    tools_dir = REPO_ROOT / "tools"
    sections.append(describe_files("Tooling scripts", iter_files(tools_dir, ["*.ps1", "*.py"]), REPO_ROOT))

    # MCP configurations
    mcp_lines: List[str] = ["### MCP configurations", ""]
    codex_config = Path.home() / ".codex" / "config.toml"
    mcp_lines.append(f"- `~/.codex/config.toml` (auto-healed on scx launch)")
    claude_mcp = REPO_ROOT / "claude-code-mcp-config.json"
    entries = load_mcp_entries(claude_mcp)
    if entries:
        mcp_lines.append("- `claude-code-mcp-config.json`")
        for name, command in entries:
            cmd_info = f" -> `{command}`" if command else ""
            mcp_lines.append(f"  - `{name}`{cmd_info}")
    mcp_lines.append("")
    sections.append("\n".join(mcp_lines))

    # Projects snapshot
    projects_dir = REPO_ROOT / "projects"
    sections.append(describe_files("Active projects", iter_files(projects_dir, ["*/README*.md"]), REPO_ROOT))

    # Final instructions
    sections.append("---\n")
    sections.append("This index regenerates on every `scx` launch. Read it first to locate deeper instructions quickly.\n")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(sections), encoding="utf-8")


if __name__ == "__main__":
    main()
