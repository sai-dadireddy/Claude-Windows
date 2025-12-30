#!/usr/bin/env python3
"""Oracle RAG - Query Oracle/PeopleSoft documentation with MOS KB support"""

import os, json, sys, re
from pathlib import Path
from typing import List, Dict, Optional

DOCS_DIR = Path(__file__).parent
PUBLIC_DIR = DOCS_DIR / "public"
PRIVATE_DIR = DOCS_DIR / "private"
PEOPLETOOLS_DIR = DOCS_DIR / "peopletools"
INTEGRATION_DIR = DOCS_DIR / "integration"
PATCHES_DIR = DOCS_DIR / "patches"

PDF_AVAILABLE = False
try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    pass

class OracleRAG:
    def __init__(self):
        self.docs = []
        self.kb_articles = {}
        self.load_docs()
        print(f"Total: {len(self.docs)} documents")

    def load_docs(self):
        """Load all document types"""
        count = 0

        # Load from all directories
        for dir_path, doc_type in [
            (PUBLIC_DIR, "public"),
            (PRIVATE_DIR, "private"),
            (PEOPLETOOLS_DIR, "peopletools"),
            (INTEGRATION_DIR, "integration"),
            (PATCHES_DIR, "patches")
        ]:
            if not dir_path.exists():
                continue

            # JSON files (API specs, KB exports)
            for f in dir_path.glob("*.json"):
                try:
                    data = json.load(open(f, encoding="utf-8"))
                    if "info" in data:  # OpenAPI spec
                        content = f"API: {data.get('info',{}).get('title','?')}\n"
                        for path, methods in data.get("paths", {}).items():
                            for m, d in methods.items():
                                if m in ["get","post","put","patch","delete"]:
                                    content += f"{m.upper()} {path} - {d.get('summary','')}\n"
                        self.docs.append({
                            "type": "openapi",
                            "category": doc_type,
                            "file": f.name,
                            "title": data.get("info",{}).get("title", f.stem),
                            "content": content
                        })
                    else:  # Generic JSON
                        self.docs.append({
                            "type": "json",
                            "category": doc_type,
                            "file": f.name,
                            "title": f.stem.replace("_", " ").title(),
                            "content": json.dumps(data, indent=2)[:10000]
                        })
                    count += 1
                except Exception as e:
                    pass

            # Text files (KB articles, guides)
            for f in dir_path.glob("*.txt"):
                try:
                    content = open(f, encoding="utf-8").read()
                    title = f.stem.replace("_", " ").replace("-", " ").title()

                    # Check for MOS KB article pattern
                    kb_match = re.search(r'(KB\d+|Doc ID:\s*\d+\.?\d*)', content[:500], re.I)
                    if kb_match:
                        kb_id = kb_match.group(1)
                        self.kb_articles[kb_id] = f.name

                    self.docs.append({
                        "type": "text",
                        "category": doc_type,
                        "file": f.name,
                        "title": title,
                        "content": content
                    })
                    count += 1
                except:
                    pass

            # PDF files
            if PDF_AVAILABLE:
                for f in dir_path.glob("*.pdf"):
                    try:
                        doc = fitz.open(f)
                        text = ""
                        for page in doc:
                            text += page.get_text()[:5000]
                            if len(text) > 50000:
                                break
                        doc.close()
                        title = f.stem.replace("-", " ").replace("_", " ").title()
                        self.docs.append({
                            "type": "pdf",
                            "category": doc_type,
                            "file": f.name,
                            "title": title,
                            "content": text[:50000]
                        })
                        count += 1
                    except:
                        pass

            # HTML files
            for f in dir_path.glob("*.html"):
                try:
                    content = open(f, encoding="utf-8").read()
                    # Strip HTML tags for search
                    text = re.sub(r'<[^>]+>', ' ', content)
                    text = re.sub(r'\s+', ' ', text).strip()
                    title = f.stem.replace("_", " ").replace("-", " ").title()
                    self.docs.append({
                        "type": "html",
                        "category": doc_type,
                        "file": f.name,
                        "title": title,
                        "content": text[:50000]
                    })
                    count += 1
                except:
                    pass

        print(f"Loaded {count} docs from {len([d for d in [PUBLIC_DIR, PRIVATE_DIR, PEOPLETOOLS_DIR, INTEGRATION_DIR, PATCHES_DIR] if d.exists()])} directories")
        if self.kb_articles:
            print(f"Found {len(self.kb_articles)} MOS KB articles")

    def search(self, query: str, top_k: int = 5, category: str = None) -> List[Dict]:
        """Keyword search with optional category filter"""
        terms = set(query.lower().split())
        results = []

        for doc in self.docs:
            # Category filter
            if category and doc.get("category") != category:
                continue

            content = doc["content"].lower()
            title = doc["title"].lower()

            # Scoring
            score = 0
            score += sum(3 for t in terms if t in title)  # Title matches worth more
            score += sum(1 for t in terms if t in content)
            score += 10 if query.lower() in content else 0  # Exact match bonus
            score += 5 if query.lower() in title else 0

            if score > 0:
                results.append({"doc": doc, "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def query(self, q: str, category: str = None) -> str:
        """Query and format results"""
        results = self.search(q, category=category)
        if not results:
            return f"No results found for: {q}"

        out = [f"## Results for: {q}\n"]
        for i, r in enumerate(results, 1):
            doc = r["doc"]
            out.append(f"### {i}. {doc['title']} (score: {r['score']})")
            out.append(f"Category: {doc['category']} | Type: {doc['type']} | File: {doc['file']}")
            snippet = doc["content"][:500] + "..." if len(doc["content"]) > 500 else doc["content"]
            out.append(f"```\n{snippet}\n```\n")
        return "\n".join(out)

    def list_docs(self, category: str = None) -> str:
        """List all indexed documents"""
        lines = ["## Oracle Documentation Index\n"]

        by_category = {}
        for doc in self.docs:
            cat = doc.get("category", "other")
            if category and cat != category:
                continue
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(doc)

        for cat, docs in sorted(by_category.items()):
            lines.append(f"\n### {cat.title()} ({len(docs)} docs)")
            for doc in docs[:20]:  # Limit display
                lines.append(f"  - [{doc['type']}] {doc['title']} ({doc['file']})")
            if len(docs) > 20:
                lines.append(f"  ... and {len(docs) - 20} more")

        lines.append(f"\nTotal: {len(self.docs)} documents")
        return "\n".join(lines)

    def list_kb_articles(self) -> str:
        """List MOS KB articles"""
        if not self.kb_articles:
            return "No MOS KB articles found. Add .txt files with KB IDs to private/"

        lines = ["## MOS KB Articles\n"]
        for kb_id, filename in sorted(self.kb_articles.items()):
            lines.append(f"  - {kb_id}: {filename}")
        lines.append(f"\nTotal: {len(self.kb_articles)} KB articles")
        return "\n".join(lines)

    def get_kb(self, kb_id: str) -> str:
        """Get specific KB article content"""
        # Normalize KB ID
        kb_id = kb_id.upper().replace(" ", "")
        if not kb_id.startswith("KB"):
            kb_id = f"KB{kb_id}"

        for doc in self.docs:
            if kb_id in doc["file"].upper() or kb_id in doc["content"][:1000].upper():
                return f"## {doc['title']}\n\nFile: {doc['file']}\n\n{doc['content'][:5000]}"

        return f"KB article '{kb_id}' not found. Use --list-kb to see available articles."

def main():
    rag = OracleRAG()

    if len(sys.argv) < 2:
        print("Oracle RAG - Query Oracle/PeopleSoft documentation")
        print("\nUsage:")
        print("  python oracle_rag.py 'query'           # Search all docs")
        print("  python oracle_rag.py --list            # List all indexed docs")
        print("  python oracle_rag.py --list-kb         # List MOS KB articles")
        print("  python oracle_rag.py --kb <id>         # Get specific KB article")
        print("  python oracle_rag.py --category <cat>  # Filter by category")
        print("  python oracle_rag.py --interactive     # Interactive mode")
        print("\nCategories: public, private, peopletools, integration, patches")
        return

    arg = sys.argv[1]

    if arg == "--list":
        cat = sys.argv[2] if len(sys.argv) > 2 else None
        print(rag.list_docs(cat))
    elif arg == "--list-kb":
        print(rag.list_kb_articles())
    elif arg == "--kb":
        if len(sys.argv) > 2:
            print(rag.get_kb(sys.argv[2]))
        else:
            print("Usage: oracle_rag.py --kb <KB_ID>")
    elif arg == "--category":
        if len(sys.argv) > 3:
            print(rag.query(" ".join(sys.argv[3:]), category=sys.argv[2]))
        else:
            print("Usage: oracle_rag.py --category <cat> <query>")
    elif arg == "--interactive":
        print("Oracle RAG Interactive (quit to exit)")
        while True:
            try:
                q = input("\n> ").strip()
                if q.lower() in ["quit", "exit", "q"]:
                    break
                if q.startswith("--"):
                    if q == "--list":
                        print(rag.list_docs())
                    elif q == "--list-kb":
                        print(rag.list_kb_articles())
                    elif q.startswith("--kb "):
                        print(rag.get_kb(q[5:].strip()))
                elif q:
                    print(rag.query(q))
            except (KeyboardInterrupt, EOFError):
                break
    else:
        print(rag.query(" ".join(sys.argv[1:])))

if __name__ == "__main__":
    main()
