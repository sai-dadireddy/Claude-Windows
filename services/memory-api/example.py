#!/usr/bin/env python3
"""
Example usage of Memory API Client

Demonstrates all available API methods:
- save_memory: Store memories with project, type, and content
- search_memories: Semantic search across memories
- promote_memory: Promote memories to global scope
- kb_retrieve: Query the Bedrock Knowledge Base
"""

from client import create_client


def main():
    # Create client (uses 'sherpa' AWS profile)
    print("Connecting to Memory API...")
    client = create_client()

    # Example 1: Save a decision
    print("\n1. Saving a decision...")
    result = client.save_memory(
        project="sherpa",
        memory_type="decision",
        content="Use TypeScript for all new frontend code to improve type safety"
    )
    print(f"   Saved: {result.get('memory_id', 'N/A')}")
    saved_memory_id = result.get('memory_id')

    # Example 2: Save a preference with metadata
    print("\n2. Saving a preference with metadata...")
    result = client.save_memory(
        project="global",
        memory_type="preference",
        content="User prefers concise code comments",
        metadata={"category": "code_style", "priority": "medium"}
    )
    print(f"   Saved: {result.get('memory_id', 'N/A')}")

    # Example 3: Save an observation
    print("\n3. Saving an observation...")
    result = client.save_memory(
        project="sherpa",
        memory_type="observation",
        content="Project uses pytest for Python tests and Jest for JavaScript tests"
    )
    print(f"   Saved: {result.get('memory_id', 'N/A')}")

    # Example 4: Search memories
    print("\n4. Searching for 'typescript' memories...")
    results = client.search_memories(
        project="sherpa",
        query="typescript frontend",
        limit=5
    )
    print(f"   Found {len(results)} results:")
    for memory in results:
        content = memory.get('content', '')[:60]
        score = memory.get('score', 0)
        print(f"   - {content}... (score: {score:.2f})")

    # Example 5: Search with type filter
    print("\n5. Searching for decisions only...")
    results = client.search_memories(
        project="sherpa",
        query="code style",
        memory_type="decision",
        limit=3
    )
    print(f"   Found {len(results)} decisions:")
    for memory in results:
        print(f"   - [{memory.get('type', 'unknown')}] {memory.get('content', '')[:50]}...")

    # Example 6: Promote a memory to global scope
    if saved_memory_id:
        print(f"\n6. Promoting memory {saved_memory_id} to global...")
        try:
            result = client.promote_memory(
                memory_id=saved_memory_id,
                target_project="global"
            )
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Target: {result.get('target_project', 'N/A')}")
        except Exception as e:
            print(f"   Error promoting memory: {e}")
    else:
        print("\n6. Skipping promote_memory (no memory_id available)")

    # Example 7: Query Knowledge Base (Bedrock)
    print("\n7. Querying Knowledge Base...")
    results = client.kb_retrieve(
        query="how to configure authentication",
        limit=3
    )
    print(f"   Found {len(results)} documents:")
    for doc in results:
        content = doc.get('content', '')[:60]
        score = doc.get('score', 0)
        print(f"   - {content}... (score: {score:.2f})")

    # Example 8: Search global memories
    print("\n8. Searching global memories...")
    results = client.search_memories(
        project="global",
        query="preferences",
        limit=5
    )
    print(f"   Found {len(results)} global memories:")
    for memory in results:
        content = memory.get('content', '')[:50]
        print(f"   - {content}...")

    print("\nDone!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
