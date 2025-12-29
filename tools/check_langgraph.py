import langgraph.checkpoint as cp
import os

print('Checkpoint path:', cp.__path__)
for p in cp.__path__:
    if os.path.exists(p):
        print(f'\nContents of {p}:')
        print(os.listdir(p))
    else:
        print(f'{p} NOT FOUND')

# Try to find SqliteSaver
print('\nTrying imports:')
try:
    from langgraph.checkpoint.sqlite import SqliteSaver
    print('✅ from langgraph.checkpoint.sqlite import SqliteSaver - WORKS')
except Exception as e:
    print(f'❌ from langgraph.checkpoint.sqlite import SqliteSaver - {e}')

try:
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
    print('✅ from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver - WORKS')
except Exception as e:
    print(f'❌ from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver - {e}')

try:
    import langgraph.checkpoint.sqlite
    print(f'✅ import langgraph.checkpoint.sqlite - WORKS')
    print(f'   Available: {dir(langgraph.checkpoint.sqlite)}')
except Exception as e:
    print(f'❌ import langgraph.checkpoint.sqlite - {e}')
