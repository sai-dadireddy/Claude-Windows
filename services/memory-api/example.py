#!/usr/bin/env python3
"""
Example usage of Memory API Client
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
    print(f"   Saved: {result['memory_id']}")

    # Example 2: Save a preference
    print("\n2. Saving a preference...")
    result = client.save_memory(
        project="global",
        memory_type="preference",
        content="User prefers concise code comments",
        metadata={"category": "code_style"}
    )
    print(f"   Saved: {result['memory_id']}")

    # Example 3: Search memories
    print("\n3. Searching for 'typescript' memories...")
    results = client.search_memories(
        project="sherpa",
        query="typescript frontend",
        limit=3
    )
    print(f"   Found {len(results)} results:")
    for memory in results:
        print(f"   - {memory['content'][:60]}... (score: {memory.get('score', 0):.2f})")

    # Example 4: List all decisions
    print("\n4. Listing recent decisions...")
    memories = client.list_memories(
        project="sherpa",
        memory_type="decision",
        limit=5
    )
    print(f"   Found {len(memories)} decisions:")
    for memory in memories:
        print(f"   - [{memory['timestamp']}] {memory['content'][:60]}...")

    # Example 5: Get specific memory (using first result from list)
    if memories:
        print(f"\n5. Retrieving memory {memories[0]['memory_id']}...")
        memory = client.get_memory(memories[0]['memory_id'])
        print(f"   Type: {memory.get('type')}")
        print(f"   Content: {memory.get('content')}")
        print(f"   Timestamp: {memory.get('timestamp')}")

    print("\nDone!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
