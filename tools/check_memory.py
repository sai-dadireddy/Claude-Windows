import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('unified-memory/databases/global.db')
cursor = conn.cursor()

# Get total count
cursor.execute('SELECT COUNT(*) FROM global_knowledge')
total = cursor.fetchone()[0]
print(f'Total knowledge entries: {total}\n')

# Get count by importance
cursor.execute('SELECT importance, COUNT(*) FROM global_knowledge GROUP BY importance ORDER BY importance DESC')
print('Knowledge by importance level:')
for row in cursor.fetchall():
    level_desc = {3: 'CRITICAL', 2: 'Important', 1: 'Useful', 0: 'Temporary'}
    print(f'  Level {row[0]} ({level_desc.get(row[0], "Unknown")}): {row[1]} entries')

# Get count by entity type
cursor.execute('SELECT entity_type, COUNT(*) FROM global_knowledge GROUP BY entity_type ORDER BY COUNT(*) DESC')
print('\nKnowledge by entity type:')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]} entries')

# Get recent entries
cursor.execute('SELECT created_at, entity_name, entity_type, importance, tags FROM global_knowledge ORDER BY created_at DESC LIMIT 15')
print('\nMost recent 15 knowledge entries:')
for row in cursor.fetchall():
    name = row[1][:60] + '...' if len(row[1]) > 60 else row[1]
    tags = row[4] if row[4] else 'no tags'
    print(f'  [{row[3]}] {row[0]} - {row[2]}: {name}')
    if tags and tags != 'no tags':
        print(f'      Tags: {tags}')

# Get critical entries
cursor.execute('SELECT entity_name, created_at, tags, content FROM global_knowledge WHERE importance = 3 ORDER BY created_at DESC LIMIT 10')
print('\nRecent CRITICAL knowledge (importance=3):')
for row in cursor.fetchall():
    name = row[0][:60] + '...' if len(row[0]) > 60 else row[0]
    tags = row[2] if row[2] else 'no tags'
    content_preview = row[3][:100] + '...' if row[3] and len(row[3]) > 100 else row[3]
    print(f'  {row[1]}: {name}')
    print(f'      Tags: {tags}')
    print(f'      Content: {content_preview}')
    print()

# Get entries by tag
cursor.execute("SELECT tags, COUNT(*) as count FROM global_knowledge WHERE tags IS NOT NULL AND tags != '' GROUP BY tags ORDER BY count DESC LIMIT 15")
print('Top tags:')
for row in cursor.fetchall():
    print(f'  {row[1]} entries: {row[0]}')

conn.close()
print('\nMemory check complete!')
