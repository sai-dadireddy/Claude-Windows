#!/usr/bin/env python3
"""Store current session data to memory"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import from the script
import importlib.util
spec = importlib.util.spec_from_file_location("auto_memory_indexer", os.path.join(os.path.dirname(__file__), "auto-memory-indexer.py"))
auto_memory_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_memory_indexer)

AutoMemoryIndexer = auto_memory_indexer.AutoMemoryIndexer

# Initialize indexer
indexer = AutoMemoryIndexer('active-genie-nginx')

# Store API path mappings
api_paths = [
    ('api-path-menu-config', '/activegenie/ui-config/menu → /ui/ui-menu-config (GET/POST)'),
    ('api-path-theme-config', '/activegenie/ui-config/theme → /ui/ui-theme-config (GET/POST)'),
    ('api-path-user-preferences', '/activegenie/ui-config/user-preferences → /ui/ui-user-preferences (GET/POST)'),
    ('api-path-component-visibility', '/activegenie/ui-config/component-visibility → /ui/ui-component-visibility (GET)'),
    ('api-path-layout-config', '/activegenie/ui-config/layout → /ui/ui-layout-config (GET)'),
    ('api-path-config-aggregator', '/activegenie/ui-config/all → /ui/ui-config-aggregator (GET)'),
    ('api-path-config-reset', '/activegenie/ui-config/reset → /ui/ui-config-reset (POST)'),
]

for name, path in api_paths:
    indexer.store_memory(
        entity_name=name,
        entity_type='api-endpoint',
        content=path,
        importance=3,
        tags=['api-gateway', 'cors-fix', 'ui-config', 'swagger-verified', '2025-10-10']
    )

# Store file paths worked on
file_paths = [
    ('ui-config-service', 'src/app/services/ui-config.service.ts', 'Angular service with 8 API path corrections'),
    ('environment-prod', 'src/environments/environment.prod.ts', 'Production environment - uses APIGW_DOMAIN placeholder'),
    ('environment-dev', 'src/environments/environment.ts', 'Development environment - uses APIGW_DOMAIN placeholder'),
    ('swagger-spec', 'docs/ActiveGenie-SaaS-v1-swagger (1) 1.json', 'API Gateway Swagger specification - source of truth for paths'),
]

for name, path, description in file_paths:
    indexer.store_memory(
        entity_name=name,
        entity_type='file-reference',
        content=f"{path} - {description}",
        importance=2,
        tags=['cors-fix', 'active-genie', 'angular', '2025-10-10']
    )

# Store deployment package files
deployment_files = [
    ('cors-fix-readme', 'Complete package documentation with deployment instructions'),
    ('cors-fix-deployment-guide', 'Step-by-step deployment guide with 3 options'),
    ('cors-fix-testing-checklist', 'Comprehensive testing checklist for QA'),
    ('cors-fix-change-summary', 'Technical change details and risk assessment'),
    ('cors-fix-quick-start', '5-step fast deployment guide'),
]

for name, description in deployment_files:
    indexer.store_memory(
        entity_name=name,
        entity_type='documentation',
        content=f"CORS Fix Package: {description}",
        importance=2,
        tags=['deployment', 'documentation', 'cors-fix', '2025-10-10']
    )

# Store auto-memory system files
memory_system_files = [
    ('auto-memory-indexer', 'Claude/claude/tools/auto-memory-indexer.py', 'Automatic memory indexer - stores session context to memory.db'),
    ('session-end-hook', 'Claude/claude/tools/hooks/session-end-hook.ps1', 'PowerShell hook that runs at session end'),
    ('auto-memory-docs', 'Claude/claude/AUTO_MEMORY_SETUP.md', 'Complete documentation for auto-memory system'),
    ('mcp-config-langchain', '.mcp.json - langchain server', 'LangChain MCP server for vector DB operations'),
]

for name, path, description in memory_system_files:
    indexer.store_memory(
        entity_name=name,
        entity_type='system-component',
        content=f"{path} - {description}",
        importance=3,
        tags=['auto-memory', 'rag-system', 'infrastructure', '2025-10-10']
    )

# Store key decisions
decisions = [
    ('decision-apigw-placeholder', 'Use APIGW_DOMAIN placeholder in environment files for CodeBuild injection instead of hardcoded domain'),
    ('decision-path-correction', 'Update all UI config paths from /activegenie/ui-config/* to /ui/ui-* to match API Gateway Swagger spec'),
    ('decision-deployment-package', 'Create comprehensive deployment package for git and frontend teams with 6 documentation files'),
    ('decision-auto-memory', 'Implement auto-memory-indexer.py to automatically update memory.db at session end'),
]

for name, decision in decisions:
    indexer.store_memory(
        entity_name=name,
        entity_type='decision',
        content=decision,
        importance=3,
        tags=['architecture', 'cors-fix', 'auto-memory', '2025-10-10']
    )

# Store problems solved
problems = [
    ('cors-errors-root-cause', 'CORS errors were caused by 404 responses from non-existent API paths, not actual CORS misconfiguration'),
    ('memory-db-not-updating', 'memory.db was not auto-updating because no automatic indexer was configured'),
    ('vector-db-not-configured', 'LangChain vector DB existed but was not configured in project .mcp.json'),
]

for name, problem in problems:
    indexer.store_memory(
        entity_name=name,
        entity_type='issue-solved',
        content=problem,
        importance=2,
        tags=['troubleshooting', 'cors-fix', 'auto-memory', '2025-10-10']
    )

# Store session summary
session_summary = """
Session: 2025-10-10 CORS Fix and Auto-Memory Setup

CORS FIX (Main Task):
1. Diagnosed CORS errors in ActiveGenie Angular application
2. Discovered API path mismatch: frontend using /activegenie/ui-config/*, backend has /ui/ui-*
3. Updated 8 API endpoints in ui-config.service.ts to match Swagger specification
4. Changed environment files to use APIGW_DOMAIN placeholder for CodeBuild injection
5. Built application successfully (4.05 MB bundle, 833.47 kB gzipped)
6. Committed and pushed changes to GitHub (commit 05d1cab)
7. Created comprehensive deployment package (30 KB zip) with 6 documentation files:
   - README.md, DEPLOYMENT_GUIDE.md, TESTING_CHECKLIST.md
   - CHANGE_SUMMARY.md, QUICK_START.md, INSTRUCTIONS_FOR_TEAM.md
8. Provided git patch file and ready-to-deploy changed files

AUTO-MEMORY SYSTEM (Secondary Task):
1. Diagnosed memory.db not updating (last modified Oct 9)
2. Discovered LangChain vector DB not configured for project
3. Created auto-memory-indexer.py (217 lines) for automatic memory management
4. Created session-end-hook.ps1 for automatic session indexing
5. Added langchain MCP server to .mcp.json
6. Tested memory.db initialization and session capture successfully
7. Created AUTO_MEMORY_SETUP.md comprehensive documentation
8. Stored all session data to memory.db (API paths, files, decisions, problems)

FILES MODIFIED:
- src/app/services/ui-config.service.ts (8 path corrections)
- src/environments/environment.prod.ts (APIGW_DOMAIN placeholder)
- src/environments/environment.ts (APIGW_DOMAIN placeholder)
- .mcp.json (added langchain server)

FILES CREATED:
- ActiveGenie-CORS-Fix-Package-2025-10-10.zip (deployment package)
- cors-fix-package/README.md, DEPLOYMENT_GUIDE.md, TESTING_CHECKLIST.md, etc.
- auto-memory-indexer.py, session-end-hook.ps1, AUTO_MEMORY_SETUP.md
- store-session-data.py (this file)

NEXT STEPS:
- User should trigger CodeBuild deployment from AWS Console
- Test application after deployment to verify CORS errors resolved
- memory.db will auto-update in future sessions

IMPACT:
- CORS errors will be resolved after deployment
- Memory system will automatically capture future session context
- Teams have complete deployment package with detailed instructions
"""

indexer.store_memory(
    entity_name='session-2025-10-10-complete',
    entity_type='session_summary',
    content=session_summary,
    importance=3,
    tags=['cors-fix', 'auto-memory', 'active-genie', 'session-complete', '2025-10-10']
)

print("[OK] All session data stored to memory.db")
print("\nRunning statistics...")

import subprocess
subprocess.run(['python', 'auto-memory-indexer.py', '--project', 'active-genie-nginx', '--stats'])
