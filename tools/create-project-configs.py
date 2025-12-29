#!/usr/bin/env python3
"""
Create .claude-project.md for all registered projects

This script generates project-specific Claude configuration files
based on the template and project information from the registry.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# UTF-8 for emojis
sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude")
PROJECTS_DB = BASE / "unified-memory/databases/projects-index.db"
TEMPLATE_PATH = BASE / "templates/.claude-project-template.md"
DOCUMENTS_ROOT = BASE / "documents"

def get_all_projects():
    """Get all registered projects from database"""
    conn = sqlite3.connect(PROJECTS_DB)
    cursor = conn.execute("""
        SELECT name, display_name, path, description
        FROM projects
        WHERE status = 'active'
        ORDER BY name
    """)
    projects = cursor.fetchall()
    conn.close()
    return projects

def create_project_config(name, display_name, path, description):
    """Create .claude-project.md for a specific project"""

    project_path = Path(path)
    config_file = project_path / ".claude-project.md"

    # Read template
    if not TEMPLATE_PATH.exists():
        print(f"❌ Template not found: {TEMPLATE_PATH}")
        return False

    template = TEMPLATE_PATH.read_text(encoding='utf-8')

    # Replace placeholders
    config_content = template.replace("[PROJECT_NAME]", display_name or name)
    config_content = config_content.replace("[project-name]", name)
    config_content = config_content.replace("[DATE]", datetime.now().strftime('%Y-%m-%d'))

    # Detect project type based on files
    project_type = detect_project_type(project_path)
    config_content = config_content.replace("[PROJECT_TYPE - e.g., Web App, API, Data Pipeline, Infrastructure]", project_type)

    # Add description if available
    if description:
        config_content = config_content.replace(
            "## Project Context",
            f"**Description:** {description}\n\n## Project Context"
        )

    # Detect technology stack
    tech_stack = detect_tech_stack(project_path)
    config_content = config_content.replace("[Language]", tech_stack.get('language', 'Unknown'))
    config_content = config_content.replace("[Framework]", tech_stack.get('framework', 'Unknown'))
    config_content = config_content.replace("[Database]", tech_stack.get('database', 'Unknown'))

    # Set absolute path
    config_content = config_content.replace("[Absolute path to project]", str(project_path))
    config_content = config_content.replace("[project-folder]", project_path.name)

    # Write config file
    try:
        config_file.write_text(config_content, encoding='utf-8')
        print(f"✅ Created: {config_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create {config_file}: {e}")
        return False

def detect_project_type(project_path):
    """Detect project type based on files"""

    if (project_path / "package.json").exists():
        pkg_json = (project_path / "package.json").read_text(encoding='utf-8')
        if '"react"' in pkg_json or '"next"' in pkg_json:
            return "Web Application (React)"
        elif '"express"' in pkg_json or '"fastify"' in pkg_json:
            return "API Server (Node.js)"
        elif '"vue"' in pkg_json:
            return "Web Application (Vue)"
        else:
            return "Node.js Project"

    if (project_path / "requirements.txt").exists() or (project_path / "setup.py").exists():
        return "Python Application"

    if (project_path / "go.mod").exists():
        return "Go Application"

    if (project_path / "Cargo.toml").exists():
        return "Rust Application"

    if (project_path / "pom.xml").exists():
        return "Java Application"

    if (project_path / ".terraform").exists() or (project_path / "main.tf").exists():
        return "Infrastructure as Code (Terraform)"

    if (project_path / ".cloudformation").exists():
        return "Infrastructure as Code (CloudFormation)"

    return "General Project"

def detect_tech_stack(project_path):
    """Detect technology stack"""

    stack = {
        'language': 'Unknown',
        'framework': 'None',
        'database': 'Unknown'
    }

    # Language detection
    if (project_path / "package.json").exists():
        stack['language'] = 'JavaScript/TypeScript'

        # Framework detection
        pkg_json_path = project_path / "package.json"
        try:
            import json
            pkg_data = json.loads(pkg_json_path.read_text(encoding='utf-8'))
            deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}

            if 'react' in deps:
                stack['framework'] = 'React'
            elif 'vue' in deps:
                stack['framework'] = 'Vue'
            elif 'express' in deps:
                stack['framework'] = 'Express.js'
            elif 'next' in deps:
                stack['framework'] = 'Next.js'

            # Database detection
            if 'pg' in deps or 'postgres' in deps:
                stack['database'] = 'PostgreSQL'
            elif 'mysql' in deps or 'mysql2' in deps:
                stack['database'] = 'MySQL'
            elif 'mongodb' in deps or 'mongoose' in deps:
                stack['database'] = 'MongoDB'
            elif 'sqlite3' in deps or 'better-sqlite3' in deps:
                stack['database'] = 'SQLite'
        except:
            pass

    elif (project_path / "requirements.txt").exists():
        stack['language'] = 'Python'

        req_text = (project_path / "requirements.txt").read_text(encoding='utf-8').lower()
        if 'django' in req_text:
            stack['framework'] = 'Django'
        elif 'flask' in req_text:
            stack['framework'] = 'Flask'
        elif 'fastapi' in req_text:
            stack['framework'] = 'FastAPI'

        if 'psycopg2' in req_text:
            stack['database'] = 'PostgreSQL'
        elif 'pymysql' in req_text:
            stack['database'] = 'MySQL'
        elif 'pymongo' in req_text:
            stack['database'] = 'MongoDB'

    elif (project_path / "go.mod").exists():
        stack['language'] = 'Go'

    elif (project_path / "Cargo.toml").exists():
        stack['language'] = 'Rust'

    elif (project_path / "pom.xml").exists():
        stack['language'] = 'Java'

    return stack

def create_document_folders(name):
    """Create document folder structure for a project"""

    project_docs = DOCUMENTS_ROOT / name

    folders = [
        'architecture',
        'api',
        'reports',
        'guides',
        'artifacts',
        'research',
        'planning'
    ]

    try:
        project_docs.mkdir(parents=True, exist_ok=True)

        for folder in folders:
            (project_docs / folder).mkdir(exist_ok=True)

        # Create README
        readme = project_docs / "README.md"
        readme_content = f"""# {name.replace('-', ' ').title()} - Documentation

This folder contains all documents, artifacts, and deliverables for the {name} project.

## Folder Structure

- **architecture/** - System designs, ADRs, architecture diagrams
- **api/** - API specifications, schemas, contracts
- **reports/** - Analysis reports, status updates, metrics
- **guides/** - User guides, developer guides, runbooks, tutorials
- **artifacts/** - Code samples, configurations, scripts, examples
- **research/** - Research notes, feasibility studies, spike results
- **planning/** - Project plans, roadmaps, timelines, milestones

## Naming Convention

Use descriptive names with dates:
```
architecture/auth-system-design-2025-09-30.md
api/user-api-spec-v1.2.md
reports/performance-analysis-2025-Q4.md
guides/deployment-runbook.md
```

## Metadata Template

Each document should include:
```markdown
---
title: Document Title
date: YYYY-MM-DD
author: Claude + [User Name]
project: {name}
category: [architecture|api|report|guide|artifact|research|planning]
status: [draft|review|final]
---
```

---

**Created:** {datetime.now().strftime('%Y-%m-%d')}
**Project:** {name}
"""
        readme.write_text(readme_content, encoding='utf-8')

        print(f"📁 Created document folders: documents/{name}/")
        return True

    except Exception as e:
        print(f"❌ Failed to create document folders for {name}: {e}")
        return False

def main():
    print("=" * 60)
    print("CREATE PROJECT CONFIGURATIONS")
    print("=" * 60)

    # Ensure documents root exists
    DOCUMENTS_ROOT.mkdir(exist_ok=True)
    print(f"\n📂 Documents root: {DOCUMENTS_ROOT}")

    # Get all projects
    projects = get_all_projects()
    print(f"\n📋 Found {len(projects)} active projects\n")

    success_count = 0
    skip_count = 0

    for name, display_name, path, description in projects:
        print(f"\n{'='*60}")
        print(f"Project: {display_name or name}")
        print(f"ID: {name}")
        print(f"Path: {path}")

        # Create .claude-project.md
        project_path = Path(path)
        config_file = project_path / ".claude-project.md"

        if config_file.exists():
            print(f"⚠️  Config exists: {config_file}")
            print("   (Skipping - delete manually to regenerate)")
            skip_count += 1
        else:
            if create_project_config(name, display_name, path, description):
                success_count += 1

        # Create document folders
        create_document_folders(name)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Created: {success_count} configs")
    print(f"⚠️  Skipped: {skip_count} (already exist)")
    print(f"📁 Document folders: {len(projects)} projects")

    print(f"\nDocument structure:")
    print(f"  {DOCUMENTS_ROOT}/")
    for name, _, _, _ in projects:
        print(f"  ├── {name}/")
        print(f"  │   ├── architecture/")
        print(f"  │   ├── api/")
        print(f"  │   ├── reports/")
        print(f"  │   ├── guides/")
        print(f"  │   ├── artifacts/")
        print(f"  │   ├── research/")
        print(f"  │   └── planning/")

    print("\n✅ All projects configured!")
    print("\n📝 Next steps:")
    print("1. Review generated .claude-project.md files")
    print("2. Customize project-specific settings")
    print("3. Update technology stack details")
    print("4. Add project-specific rules and patterns")

if __name__ == "__main__":
    main()