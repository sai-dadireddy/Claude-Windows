#!/usr/bin/env python3
"""
Workday RAG - Simple agentic RAG for Workday API documentation
Usage: python workday_rag.py "How do I create a payment term?"
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import re

# Configuration
DOCS_DIR = Path(__file__).parent
PUBLIC_DIR = DOCS_DIR / "public"
PRIVATE_DIR = DOCS_DIR / "private"

class WorkdayRAG:
    def __init__(self):
        self.docs: List[Dict] = []
        self.load_docs()

    def load_docs(self):
        """Load all documentation files"""
        # Load JSON specs (OpenAPI)
        for json_file in PUBLIC_DIR.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    spec = json.load(f)
                self.docs.append({
                    'type': 'openapi',
                    'file': json_file.name,
                    'title': spec.get('info', {}).get('title', json_file.stem),
                    'content': self._flatten_openapi(spec),
                    'raw': spec
                })
            except Exception as e:
                print(f"Warning: Could not load {json_file}: {e}")

        # Load text/markdown files
        for txt_file in PRIVATE_DIR.glob("*.txt"):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.docs.append({
                    'type': 'text',
                    'file': txt_file.name,
                    'title': txt_file.stem.replace('_', ' ').title(),
                    'content': content
                })
            except Exception as e:
                print(f"Warning: Could not load {txt_file}: {e}")

        print(f"Loaded {len(self.docs)} documents")

    def _flatten_openapi(self, spec: dict) -> str:
        """Convert OpenAPI spec to searchable text"""
        lines = []
        info = spec.get('info', {})
        lines.append(f"API: {info.get('title', 'Unknown')}")
        lines.append(f"Version: {info.get('version', 'Unknown')}")
        lines.append(f"Description: {info.get('description', '')[:500]}")

        # Extract endpoints
        for path, methods in spec.get('paths', {}).items():
            for method, details in methods.items():
                if method in ['get', 'post', 'put', 'patch', 'delete']:
                    summary = details.get('summary', details.get('operationId', ''))
                    lines.append(f"{method.upper()} {path} - {summary}")

        # Extract schemas
        for name, schema in spec.get('components', {}).get('schemas', {}).items():
            props = list(schema.get('properties', {}).keys())
            lines.append(f"Schema {name}: {', '.join(props[:10])}")

        return '\n'.join(lines)

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Simple keyword search (can be upgraded to semantic)"""
        query_terms = set(query.lower().split())
        results = []

        for doc in self.docs:
            content_lower = doc['content'].lower()
            # Score by term matches
            score = sum(1 for term in query_terms if term in content_lower)
            # Boost exact phrase matches
            if query.lower() in content_lower:
                score += 5

            if score > 0:
                results.append({
                    'doc': doc,
                    'score': score,
                    'snippet': self._extract_snippet(doc['content'], query)
                })

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

    def _extract_snippet(self, content: str, query: str, window: int = 200) -> str:
        """Extract relevant snippet around query terms"""
        query_lower = query.lower()
        content_lower = content.lower()

        # Find first occurrence of any query term
        pos = -1
        for term in query.lower().split():
            idx = content_lower.find(term)
            if idx != -1 and (pos == -1 or idx < pos):
                pos = idx

        if pos == -1:
            return content[:window] + "..."

        start = max(0, pos - window // 2)
        end = min(len(content), pos + window // 2)
        snippet = content[start:end]

        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."

        return snippet

    def query(self, question: str) -> str:
        """Main query interface"""
        results = self.search(question)

        if not results:
            return "No relevant documentation found. Try different keywords."

        # Build response
        response = [f"## Results for: {question}\n"]

        for i, r in enumerate(results, 1):
            doc = r['doc']
            response.append(f"### {i}. {doc['title']} (score: {r['score']})")
            response.append(f"Source: {doc['file']}")
            response.append(f"```\n{r['snippet']}\n```\n")

        # If OpenAPI doc, try to extract specific endpoint
        for r in results:
            if r['doc']['type'] == 'openapi' and 'raw' in r['doc']:
                endpoint_info = self._find_endpoint(r['doc']['raw'], question)
                if endpoint_info:
                    response.append(f"### Relevant Endpoint\n{endpoint_info}")
                    break

        return '\n'.join(response)

    def _find_endpoint(self, spec: dict, query: str) -> Optional[str]:
        """Find specific endpoint matching query"""
        query_lower = query.lower()

        for path, methods in spec.get('paths', {}).items():
            for method, details in methods.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                summary = details.get('summary', '').lower()
                op_id = details.get('operationId', '').lower()

                if any(term in summary or term in op_id or term in path.lower()
                       for term in query_lower.split()):
                    return f"""
**{method.upper()} {path}**
Summary: {details.get('summary', 'N/A')}
Operation: {details.get('operationId', 'N/A')}
"""
        return None

    def list_endpoints(self, api_name: str = None) -> str:
        """List all available endpoints"""
        lines = ["## Available Endpoints\n"]

        for doc in self.docs:
            if doc['type'] != 'openapi':
                continue
            if api_name and api_name.lower() not in doc['title'].lower():
                continue

            lines.append(f"### {doc['title']}")
            spec = doc.get('raw', {})

            for path, methods in spec.get('paths', {}).items():
                for method, details in methods.items():
                    if method in ['get', 'post', 'put', 'patch', 'delete']:
                        lines.append(f"  {method.upper():6} {path}")
            lines.append("")

        return '\n'.join(lines)


def main():
    rag = WorkdayRAG()

    if len(sys.argv) < 2:
        print("Workday RAG - Query your Workday API documentation")
        print("\nUsage:")
        print("  python workday_rag.py 'your question'")
        print("  python workday_rag.py --list              # List all endpoints")
        print("  python workday_rag.py --interactive       # Interactive mode")
        print("\nExamples:")
        print("  python workday_rag.py 'how to create payment term'")
        print("  python workday_rag.py 'authentication headers'")
        return

    if sys.argv[1] == '--list':
        print(rag.list_endpoints())
    elif sys.argv[1] == '--interactive':
        print("Workday RAG Interactive Mode (type 'quit' to exit)")
        while True:
            try:
                q = input("\n> ").strip()
                if q.lower() in ['quit', 'exit', 'q']:
                    break
                if q:
                    print(rag.query(q))
            except (KeyboardInterrupt, EOFError):
                break
    else:
        question = ' '.join(sys.argv[1:])
        print(rag.query(question))


if __name__ == '__main__':
    main()
