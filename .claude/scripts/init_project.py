#!/usr/bin/env python3
"""
Initialize a new project with CLAUDE.md and optionally Beads

Usage:
    python3 C:/Users/SainathreddyDadiredd/.claude/scripts/init_project.py [project_path]
    python3 C:/Users/SainathreddyDadiredd/.claude/scripts/init_project.py --with-beads [project_path]

This script:
1. Detects project type (Node, Python, Rust, Go, etc.)
2. Generates appropriate CLAUDE.md
3. Optionally initializes Beads
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

TEMPLATE_PATH = Path.home() / ".claude" / "templates" / "PROJECT_CLAUDE.md"

def detect_project_type(project_path: Path) -> dict:
    """Detect project type based on config files."""

    info = {
        "language": "Unknown",
        "framework": "Unknown",
        "dev_command": "# Add dev command",
        "test_command": "# Add test command",
        "build_command": "# Add build command",
        "lint_command": "# Add lint command",
        "main_file": "",
        "config_file": "",
        "protected_dirs": [],
        "conventions": []
    }

    # Node.js / TypeScript
    if (project_path / "package.json").exists():
        info["language"] = "TypeScript/JavaScript"
        info["config_file"] = "package.json"

        try:
            pkg = json.loads((project_path / "package.json").read_text())
            scripts = pkg.get("scripts", {})

            if "dev" in scripts:
                info["dev_command"] = "npm run dev"
            elif "start" in scripts:
                info["dev_command"] = "npm start"

            if "test" in scripts:
                info["test_command"] = "npm test"

            if "build" in scripts:
                info["build_command"] = "npm run build"

            if "lint" in scripts:
                info["lint_command"] = "npm run lint"

            # Detect framework
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                info["framework"] = "Next.js"
                info["main_file"] = "src/app/page.tsx or pages/index.tsx"
            elif "react" in deps:
                info["framework"] = "React"
                info["main_file"] = "src/App.tsx or src/index.tsx"
            elif "vue" in deps:
                info["framework"] = "Vue.js"
                info["main_file"] = "src/App.vue"
            elif "express" in deps:
                info["framework"] = "Express.js"
                info["main_file"] = "src/index.ts or app.ts"
            elif "fastify" in deps:
                info["framework"] = "Fastify"
                info["main_file"] = "src/index.ts"

        except:
            pass

        info["protected_dirs"] = ["node_modules", "dist", ".next"]
        info["conventions"] = [
            "Use ES modules (import/export)",
            "Prefer async/await over callbacks",
            "Use TypeScript strict mode"
        ]

    # Python
    elif (project_path / "pyproject.toml").exists() or (project_path / "setup.py").exists():
        info["language"] = "Python"
        info["config_file"] = "pyproject.toml" if (project_path / "pyproject.toml").exists() else "setup.py"
        info["dev_command"] = "python -m uvicorn main:app --reload" if (project_path / "main.py").exists() else "python main.py"
        info["test_command"] = "pytest"
        info["build_command"] = "pip install -e ."
        info["lint_command"] = "ruff check . && ruff format --check ."

        # Detect framework
        if (project_path / "pyproject.toml").exists():
            try:
                content = (project_path / "pyproject.toml").read_text()
                if "fastapi" in content.lower():
                    info["framework"] = "FastAPI"
                    info["main_file"] = "main.py or app/main.py"
                elif "django" in content.lower():
                    info["framework"] = "Django"
                    info["main_file"] = "manage.py"
                elif "flask" in content.lower():
                    info["framework"] = "Flask"
                    info["main_file"] = "app.py"
            except:
                pass

        info["protected_dirs"] = ["venv", ".venv", "__pycache__", ".pytest_cache"]
        info["conventions"] = [
            "Use type hints for function signatures",
            "Follow PEP 8 style guide",
            "Use pathlib for file operations"
        ]

    # Rust
    elif (project_path / "Cargo.toml").exists():
        info["language"] = "Rust"
        info["framework"] = "Cargo"
        info["config_file"] = "Cargo.toml"
        info["main_file"] = "src/main.rs or src/lib.rs"
        info["dev_command"] = "cargo run"
        info["test_command"] = "cargo test"
        info["build_command"] = "cargo build --release"
        info["lint_command"] = "cargo clippy"
        info["protected_dirs"] = ["target"]
        info["conventions"] = [
            "Use rustfmt for formatting",
            "Handle all Result types explicitly",
            "Prefer &str over String for function parameters"
        ]

    # Go
    elif (project_path / "go.mod").exists():
        info["language"] = "Go"
        info["framework"] = "Go modules"
        info["config_file"] = "go.mod"
        info["main_file"] = "main.go or cmd/*/main.go"
        info["dev_command"] = "go run ."
        info["test_command"] = "go test ./..."
        info["build_command"] = "go build -o bin/"
        info["lint_command"] = "golangci-lint run"
        info["protected_dirs"] = ["vendor"]
        info["conventions"] = [
            "Use gofmt for formatting",
            "Handle all errors explicitly",
            "Use interfaces for dependency injection"
        ]

    return info

def get_project_structure(project_path: Path, max_depth: int = 2) -> str:
    """Generate project structure tree."""

    skip_dirs = {
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", "target", ".pytest_cache",
        ".mypy_cache", "coverage", ".idea", ".vscode"
    }

    lines = []

    def walk(path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return

        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))

        for i, item in enumerate(items):
            if item.name in skip_dirs or item.name.startswith('.'):
                continue

            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "

            if item.is_dir():
                lines.append(f"{prefix}{connector}{item.name}/")
                extension = "    " if is_last else "│   "
                walk(item, prefix + extension, depth + 1)
            else:
                lines.append(f"{prefix}{connector}{item.name}")

    walk(project_path)
    return "\n".join(lines[:30])  # Limit output

def generate_claude_md(project_path: Path, project_name: str) -> str:
    """Generate CLAUDE.md content for the project."""

    info = detect_project_type(project_path)
    structure = get_project_structure(project_path)

    content = f"""# Project: {project_name}

## Quick Start

```bash
# Development
{info['dev_command']}

# Tests
{info['test_command']}

# Build
{info['build_command']}
```

## Tech Stack

- **Language:** {info['language']}
- **Framework:** {info['framework']}
- **Config:** {info['config_file']}

## Project Structure

```
{structure}
```

## Key Files

| File | Purpose |
|------|---------|
| `{info['main_file']}` | Entry point |
| `{info['config_file']}` | Configuration |

## Coding Conventions

"""

    for conv in info['conventions']:
        content += f"- {conv}\n"

    content += f"""
## DO NOT

- Do not modify files in `{', '.join(info['protected_dirs'])}`
- Do not commit directly to `main` branch
- Do not expose secrets in code

---

## For Claude (Auto-injected at session start)

### Task Management

**Use Beads** for multi-step features:
```bash
PATH=$HOME/.local/bin:$PATH bd init
PATH=$HOME/.local/bin:$PATH bd create "Task" -t feature -p 1
PATH=$HOME/.local/bin:$PATH bd ready
```

**Use TodoWrite** for simple checklists.

### Memory

Save decisions:
```bash
C:/Users/SainathreddyDadiredd/.claude/scripts/memory_manager.py save-memory "{project_name}" decision "Decision details"
```

### Verify Before Completing

```bash
{info['test_command']}
{info['lint_command']}
```
"""

    return content

def init_beads(project_path: Path):
    """Initialize beads in the project."""
    env = os.environ.copy()
    env["PATH"] = f"{Path.home()}/.local/bin:{env.get('PATH', '')}"

    try:
        result = subprocess.run(
            ["bd", "init", "--quiet"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        return result.returncode == 0
    except:
        return False

def main():
    # Parse arguments
    with_beads = "--with-beads" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    project_path = Path(args[0]) if args else Path.cwd()
    project_path = project_path.resolve()

    if not project_path.exists():
        print(f"Error: Path does not exist: {project_path}")
        sys.exit(1)

    project_name = project_path.name

    print(f"Initializing project: {project_name}")
    print(f"Path: {project_path}")

    # Generate CLAUDE.md
    claude_md_path = project_path / "CLAUDE.md"

    if claude_md_path.exists():
        print(f"CLAUDE.md already exists at {claude_md_path}")
        response = input("Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("Skipping CLAUDE.md generation")
        else:
            content = generate_claude_md(project_path, project_name)
            claude_md_path.write_text(content)
            print(f"✅ Generated CLAUDE.md")
    else:
        content = generate_claude_md(project_path, project_name)
        claude_md_path.write_text(content)
        print(f"✅ Generated CLAUDE.md")

    # Initialize beads if requested
    if with_beads:
        print("Initializing Beads...")
        if init_beads(project_path):
            print("✅ Beads initialized")
        else:
            print("⚠️ Beads initialization failed (may already be initialized)")

    print("\nDone! Your project is ready for Claude Code.")
    print("\nNext steps:")
    print("1. Review and customize CLAUDE.md")
    print("2. Start Claude Code in the project directory")
    if not with_beads:
        print("3. Run `bd init` if you need issue tracking")

if __name__ == "__main__":
    main()
