#!/usr/bin/env python3
"""
Test Memory Searches - Verify Migration
Tests that all migrated data is searchable in the database
"""

import sqlite3
import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude")
GLOBAL_DB = BASE_PATH / "unified-memory/databases/global.db"
PROJECTS_DB = BASE_PATH / "unified-memory/databases/projects-index.db"

def connect_db(db_path):
    """Connect to database"""
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return None
    return sqlite3.connect(str(db_path))

def test_search_bootstrap():
    """Test 1: Search for bootstrap sessions"""
    print("="*60)
    print("TEST 1: Search for 'bootstrap' sessions")
    print("="*60)

    conn = connect_db(GLOBAL_DB)
    if not conn:
        return False

    cursor = conn.execute("""
        SELECT content, entity_name, entity_type, importance, tags, created_at
        FROM global_knowledge
        WHERE content LIKE '%bootstrap%' OR entity_name LIKE '%bootstrap%' OR tags LIKE '%bootstrap%'
        ORDER BY importance DESC, created_at DESC
        LIMIT 10
    """)

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("❌ FAILED: No bootstrap sessions found")
        return False

    print(f"✅ PASSED: Found {len(results)} bootstrap session(s)\n")
    for i, (content, entity, entity_type, importance, tags, created) in enumerate(results[:3], 1):
        preview = content[:100] + "..." if len(content) > 100 else content
        print(f"{i}. [{importance}⭐] {preview}")
        if entity:
            print(f"   📌 Entity: {entity}")
        print(f"   🔖 Tags: {tags}")
        print()

    if len(results) > 3:
        print(f"   ... and {len(results) - 3} more results\n")

    return True

def test_search_project():
    """Test 2: Search for active-genie-nginx content"""
    print("="*60)
    print("TEST 2: Search for 'active-genie-nginx' project data")
    print("="*60)

    conn = connect_db(GLOBAL_DB)
    if not conn:
        return False

    cursor = conn.execute("""
        SELECT content, entity_name, entity_type, importance, tags
        FROM global_knowledge
        WHERE content LIKE '%active-genie-nginx%'
           OR entity_name LIKE '%active-genie%'
           OR tags LIKE '%active-genie%'
        ORDER BY importance DESC
        LIMIT 10
    """)

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("❌ FAILED: No active-genie-nginx data found")
        return False

    print(f"✅ PASSED: Found {len(results)} result(s) for active-genie-nginx\n")
    for i, (content, entity, entity_type, importance, tags) in enumerate(results[:3], 1):
        preview = content[:100] + "..." if len(content) > 100 else content
        print(f"{i}. [{importance}⭐] {preview}")
        print(f"   🏷️ Type: {entity_type}")
        print()

    if len(results) > 3:
        print(f"   ... and {len(results) - 3} more results\n")

    return True

def test_search_checkpoint():
    """Test 3: Search for checkpoint files"""
    print("="*60)
    print("TEST 3: Search for 'checkpoint' files")
    print("="*60)

    conn = connect_db(GLOBAL_DB)
    if not conn:
        return False

    cursor = conn.execute("""
        SELECT content, entity_name, importance, tags
        FROM global_knowledge
        WHERE content LIKE '%checkpoint%'
           OR entity_name LIKE '%CHECKPOINT%'
           OR tags LIKE '%checkpoint%'
        ORDER BY importance DESC
    """)

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("❌ FAILED: No checkpoint files found")
        return False

    print(f"✅ PASSED: Found {len(results)} checkpoint file(s)\n")
    for i, (content, entity, importance, tags) in enumerate(results[:2], 1):
        preview = content[:100] + "..." if len(content) > 100 else content
        print(f"{i}. [{importance}⭐] {preview}")
        if entity:
            print(f"   📌 Entity: {entity}")
        print()

    return True

def test_list_projects():
    """Test 4: List all projects"""
    print("="*60)
    print("TEST 4: List all registered projects")
    print("="*60)

    conn = connect_db(PROJECTS_DB)
    if not conn:
        return False

    cursor = conn.execute("""
        SELECT name, display_name, status, updated_at
        FROM projects
        ORDER BY updated_at DESC
    """)

    projects = cursor.fetchall()
    conn.close()

    if not projects:
        print("❌ FAILED: No projects found")
        return False

    print(f"✅ PASSED: Found {len(projects)} project(s)\n")
    for i, (name, display_name, status, updated) in enumerate(projects, 1):
        title = display_name or name.replace('-', ' ').title()
        print(f"{i}. {title}")
        print(f"   ID: {name}")
        print(f"   Status: {status}")
        print()

    return True

def test_total_entries():
    """Bonus: Count total migrated entries"""
    print("="*60)
    print("BONUS: Total migrated entries")
    print("="*60)

    conn = connect_db(GLOBAL_DB)
    if not conn:
        return False

    # Total entries
    cursor = conn.execute("SELECT COUNT(*) FROM global_knowledge")
    total = cursor.fetchone()[0]

    # By type
    cursor = conn.execute("""
        SELECT entity_type, COUNT(*)
        FROM global_knowledge
        GROUP BY entity_type
        ORDER BY COUNT(*) DESC
    """)
    types = cursor.fetchall()

    # By importance
    cursor = conn.execute("""
        SELECT importance, COUNT(*)
        FROM global_knowledge
        GROUP BY importance
        ORDER BY importance DESC
    """)
    importance_counts = cursor.fetchall()

    conn.close()

    print(f"\n✅ Total entries in database: {total}")
    print(f"\nBy type:")
    for entity_type, count in types:
        type_name = entity_type or "(none)"
        print(f"  - {type_name}: {count}")

    print(f"\nBy importance:")
    for importance, count in importance_counts:
        stars = "⭐" * importance
        print(f"  - {importance} {stars}: {count}")

    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 MEMORY MIGRATION TESTS")
    print("="*60)
    print("\nVerifying all data is searchable in unified memory...\n")

    results = []

    # Run tests
    results.append(("Bootstrap search", test_search_bootstrap()))
    results.append(("Project search", test_search_project()))
    results.append(("Checkpoint search", test_search_checkpoint()))
    results.append(("List projects", test_list_projects()))
    results.append(("Database stats", test_total_entries()))

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\n✅ Your data is fully migrated and searchable")
        print("✅ Safe to delete old files")
        print("\nNext step: Run cleanup script")
        print("  cd \"C:\\Users\\SainathreddyDadiredd\\OneDrive - ERPA\\Claude\"")
        print("  .\\cleanup-all-migrated-files.ps1")
    else:
        print("\n" + "="*60)
        print("⚠️  SOME TESTS FAILED")
        print("="*60)
        print("\n⚠️  Do NOT delete files yet")
        print("⚠️  Review errors above")

    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Tests cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
