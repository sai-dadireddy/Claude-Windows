#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global Project Tracker Generator
Creates PROJECT-TRACKER.md for any project with initial structure

Usage: python tools/create-project-tracker.py --project-name "ERPAGPT" --project-dir "projects/erpa/erpagpt"
"""

import argparse
import sys
import io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_TRACKER_TEMPLATE = '''# 🎯 {project_name} Project Tracker (Auto-Updated)

**Last Updated**: {timestamp}
**Auto-Update**: MANDATORY at end of every task
**Source of Truth**: This file tracks ALL project status

---

## 📊 Quick Status Dashboard

| Metric | Status | Target | Notes |
|--------|--------|--------|-------|
| **Phase** | Phase 1 | Completion | Initial setup |
| **Budget** | TBD | TBD | Not yet defined |
| **Go-Live Date** | TBD | TBD | Target date TBD |
| **Completion** | 0% | 100% | Just started |

---

## 🗂️ Phase Status Matrix

### ⏳ Phase 1: Foundation (IN PROGRESS)
**Status**: Just Started
**Started**: {date}

| Component | Status | Details |
|-----------|--------|---------|
| Initial Setup | ⏳ | Setting up project structure |

**Cost**: TBD

---

## 🎯 Current Sprint (Active Tasks)

### 🔴 High Priority (Start Here)

1. **Define Project Goals** ⏳
   - **What**: Clearly define what this project aims to accomplish
   - **Why**: Establishes clear direction
   - **Time**: 30 minutes

2. **Set Up Project Structure** ⏳
   - **What**: Create initial directories, files, and tools
   - **Why**: Organized foundation
   - **Time**: 1 hour

### 🟡 Medium Priority (Next Steps)

1. **Create Initial Documentation** ⏳
   - **What**: Architecture docs, deployment guides
   - **Why**: Knowledge preservation
   - **Time**: 2 hours

---

## 📚 Essential Documentation (Keep These)

### **Active Reference** (Must Read Before Any Work):
1. **PROJECT-TRACKER.md** ← THIS FILE (Source of Truth)
2. **.claude-project.md** ← Project instructions & Git workflow
3. **README.md** ← Project overview

### **Architecture & Decisions**:
(Add architecture docs here as they're created)

### **Deployment Guides**:
(Add deployment guides here as they're created)

### **Testing**:
(Add testing guides here as they're created)

---

## 🗑️ Documentation to Archive

(As project progresses, list files to archive here)

---

## 💡 Lessons Learned (Updated After Each Task)

### Project Initialization ({date}):

#### ✅ What Went Well:
- Created PROJECT-TRACKER.md for structured management
- Set up RAG-first documentation system

#### ⚠️ Challenges Encountered:
(Will document as challenges arise)

#### 🎓 Apply to Future Tasks:
- Follow RAG-first approach from day 1
- Update this tracker after every task
- Document lessons learned immediately

---

## 🚀 Next Steps (Priority Order)

### **Immediate** (Next 30 minutes):
1. ⏳ Define project goals and scope
2. ⏳ Create .claude-project.md with project instructions
3. ⏳ Set up RAG tools (ingest, query scripts)

### **Today** (Next 2-4 hours):
4. ⏳ Create initial architecture documentation
5. ⏳ Set up development environment
6. ⏳ Create README.md

### **This Week**:
7. ⏳ [Add specific week goals]
8. ⏳ [Add more tasks]

---

## 📈 Success Metrics (Track Progress)

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| **Phase 1 Tasks Completed** | 0 | TBD | ⏳ |
| **Essential Docs Count** | 1 | 5-10 | ⏳ |
| **RAG Collection Created** | No | Yes | ⏳ |
| **Budget Usage** | $0 | TBD | ⏳ |

---

## 🔄 Auto-Update Protocol (MANDATORY)

### **When to Update This File**:
- ✅ **After completing ANY task** (change status, add lessons)
- ✅ **After encountering ANY blocker** (document in Challenges)
- ✅ **At end of every session** (update metrics, next steps)
- ✅ **Before starting new work** (check Current Sprint section)

### **How to Update**:
1. Change task status: ⏳ → ✅ or ❌
2. Update "Last Updated" timestamp at top
3. Add new lesson learned if applicable
4. Update success metrics table
5. Move completed tasks from "Current Sprint" to appropriate Phase
6. Add new blockers/challenges as they arise

### **Enforcement**:
This update protocol is **MANDATORY** and enforced via `.claude-project.md`:
- Claude Code will check this file at session start
- Claude Code will update this file after task completion
- Failure to update = incomplete task

---

## 📞 Key Contacts & Resources

| Resource | Location | Purpose |
|----------|----------|------------|
| **Project Repository** | TBD | Source code |
| **Documentation** | docs/ | All project docs |
| **RAG Collection** | projects/unified-memory/vector-store/{project_slug}/ | Knowledge base |

---

## 🎓 Project Context (For New Sessions)

### **What is {project_name}?**
(Add project description here)

### **Architecture**:
(Add architecture overview here)

### **Current State**:
- Phase 1: Just started ⏳

### **Quick Start**:
1. Read this file (PROJECT-TRACKER.md)
2. Check "Current Sprint" section for active tasks
3. Review "Lessons Learned" before starting work
4. Update this file after completing tasks

---

**🎯 Remember**: This file is the SINGLE SOURCE OF TRUTH. All other docs are secondary. Query RAG first, read files only if necessary!

---

*Auto-generated tracker | {project_name} Project | ERPA Team*
'''

def create_project_tracker(project_name: str, project_dir: str):
    """Generate PROJECT-TRACKER.md for a project."""
    project_path = Path(project_dir)

    if not project_path.exists():
        print(f"❌ Error: Project directory doesn't exist: {project_dir}")
        return False

    tracker_path = project_path / "PROJECT-TRACKER.md"

    if tracker_path.exists():
        print(f"⚠️  Warning: PROJECT-TRACKER.md already exists at {tracker_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            return False

    # Generate content
    content = PROJECT_TRACKER_TEMPLATE.format(
        project_name=project_name,
        timestamp=datetime.now().isoformat() + "Z",
        date=datetime.now().strftime("%Y-%m-%d"),
        project_slug=project_name.lower().replace(" ", "-")
    )

    # Write file
    tracker_path.write_text(content, encoding='utf-8')

    print(f"✅ Created PROJECT-TRACKER.md at {tracker_path}")
    print(f"\n📋 Next steps:")
    print(f"1. Edit PROJECT-TRACKER.md to add project-specific details")
    print(f"2. Create .claude-project.md with project instructions")
    print(f"3. Set up RAG tools (tools/ingest-project-rag.py, tools/query-project-rag.py)")
    print(f"4. Create initial RAG collection")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Generate PROJECT-TRACKER.md for any project"
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="Project name (e.g., 'ERPAGPT', 'AGUPGRADE')"
    )
    parser.add_argument(
        "--project-dir",
        required=True,
        help="Project directory path (e.g., 'projects/erpa/erpagpt')"
    )

    args = parser.parse_args()

    success = create_project_tracker(args.project_name, args.project_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
