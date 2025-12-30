#!/usr/bin/env python3
"""Workday RAG - Query Workday API documentation with WSDL support"""

import os, json, sys, pickle, hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional

DOCS_DIR = Path(__file__).parent
PUBLIC_DIR = DOCS_DIR / "public"
PRIVATE_DIR = DOCS_DIR / "private"
WSDL_DIR = DOCS_DIR / "wsdl"
EMBEDDINGS_CACHE = DOCS_DIR / "embeddings.pkl"

GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    pass

class WSDLParser:
    WSDL_NS = {"wsdl": "http://schemas.xmlsoap.org/wsdl/"}
    
    @classmethod
    def parse_file(cls, wsdl_path):
        try:
            tree = ET.parse(wsdl_path)
            root = tree.getroot()
            name = root.attrib.get("name", wsdl_path.stem)
            service_doc = ""
            for doc_elem in root.findall("wsdl:documentation", cls.WSDL_NS):
                if doc_elem.text:
                    service_doc = doc_elem.text.strip()
                    break
            operations = []
            for portType in root.findall("wsdl:portType", cls.WSDL_NS):
                for op in portType.findall("wsdl:operation", cls.WSDL_NS):
                    op_name = op.attrib.get("name", "")
                    if op_name:
                        doc_elem = op.find("wsdl:documentation", cls.WSDL_NS)
                        op_doc = doc_elem.text.strip() if doc_elem is not None and doc_elem.text else ""
                        operations.append({"name": op_name, "description": op_doc})
            return {"name": name, "file": wsdl_path.name, "description": service_doc, "operations": operations}
        except:
            return None

    @classmethod
    def format_operations(cls, wsdl_data):
        lines = [f"WSDL: {wsdl_data['name']}", f"Description: {wsdl_data['description']}", "Operations:"]
        for op in wsdl_data["operations"]:
            lines.append(f"  - {op['name']}: {op['description']}")
        return "\n".join(lines)

class WorkdayRAG:
    def __init__(self, rebuild_embeddings=False):
        self.docs = []
        self.wsdl_data = {}
        self.load_docs()
        self.load_wsdls()
        print(f"Total: {len(self.docs)} documents")

    def load_docs(self):
        if PUBLIC_DIR.exists():
            for f in PUBLIC_DIR.glob("*.json"):
                try:
                    spec = json.load(open(f, encoding="utf-8"))
                    content = f"API: {spec.get('info',{}).get('title','?')}\n"
                    for path, methods in spec.get("paths", {}).items():
                        for m, d in methods.items():
                            if m in ["get","post","put","patch","delete"]:
                                content += f"{m.upper()} {path} - {d.get('summary','')}\n"
                    self.docs.append({"type": "openapi", "file": f.name, "title": spec.get("info",{}).get("title",f.stem), "content": content, "raw": spec})
                except: pass
        if PRIVATE_DIR.exists():
            for f in PRIVATE_DIR.glob("*.txt"):
                try:
                    self.docs.append({"type": "text", "file": f.name, "title": f.stem.replace("_"," ").title(), "content": open(f, encoding="utf-8").read()})
                except: pass
        print(f"Loaded {len(self.docs)} docs from public/private")

    def load_wsdls(self):
        if not WSDL_DIR.exists():
            print("No wsdl/ directory")
            return
        count = 0
        for f in WSDL_DIR.glob("*.wsdl"):
            p = WSDLParser.parse_file(f)
            if p:
                self.wsdl_data[p["name"]] = p
                self.docs.append({"type": "wsdl", "file": f.name, "title": f"WSDL: {p['name']}", "content": WSDLParser.format_operations(p), "wsdl_name": p["name"]})
                count += 1
        total_ops = sum(len(w["operations"]) for w in self.wsdl_data.values())
        print(f"Loaded {count} WSDLs with {total_ops} operations")

    def search(self, query, top_k=3):
        terms = set(query.lower().split())
        results = []
        for doc in self.docs:
            c = doc["content"].lower()
            score = sum(1 for t in terms if t in c) + (5 if query.lower() in c else 0)
            if score > 0:
                results.append({"doc": doc, "score": score})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def query(self, q):
        results = self.search(q)
        if not results:
            return "No results found."
        out = [f"## Results for: {q}\n"]
        for i, r in enumerate(results, 1):
            out.append(f"### {i}. {r['doc']['title']} (score: {r['score']})")
            out.append(f"Source: {r['doc']['file']}")
            snippet = r["doc"]["content"][:300] + "..." if len(r["doc"]["content"]) > 300 else r["doc"]["content"]
            out.append(f"```\n{snippet}\n```\n")
        return "\n".join(out)

    def list_wsdl_operations(self, name=None):
        if name:
            for n, d in self.wsdl_data.items():
                if name.lower() in n.lower():
                    lines = [f"### {d['name']}", f"Description: {d['description']}\n", "Operations:"]
                    for op in d["operations"]:
                        lines.append(f"  {op['name']}{' - ' + op['description'] if op['description'] else ''}")
                    return "\n".join(lines)
            return f"WSDL '{name}' not found."
        lines = ["## WSDL Services\n"]
        for n, d in sorted(self.wsdl_data.items()):
            lines.append(f"  {n}: {len(d['operations'])} operations")
        lines.append(f"\nTotal: {len(self.wsdl_data)} WSDLs")
        return "\n".join(lines)

def main():
    rag = WorkdayRAG()
    if len(sys.argv) < 2:
        print("Workday RAG - Query Workday API documentation")
        print("\nUsage:")
        print("  python workday_rag.py 'query'")
        print("  python workday_rag.py --list-wsdl")
        print("  python workday_rag.py --wsdl <name>")
        print("  python workday_rag.py --interactive")
        return
    if sys.argv[1] == "--list-wsdl":
        print(rag.list_wsdl_operations())
    elif sys.argv[1] == "--wsdl":
        print(rag.list_wsdl_operations(sys.argv[2] if len(sys.argv) > 2 else None))
    elif sys.argv[1] == "--interactive":
        print("Workday RAG Interactive (quit to exit)")
        while True:
            try:
                q = input("\n> ").strip()
                if q.lower() in ["quit", "exit", "q"]:
                    break
                if q:
                    print(rag.query(q))
            except (KeyboardInterrupt, EOFError):
                break
    else:
        print(rag.query(" ".join(sys.argv[1:])))

if __name__ == "__main__":
    main()


    def _find_endpoint(self, spec: dict, query: str) -> Optional[str]:
        """Find specific endpoint matching query"""
        query_lower = query.lower()

        for path, methods in spec.get("paths", {}).items():
            for method, details in methods.items():
                if method not in ["get", "post", "put", "patch", "delete"]:
                    continue

                summary = details.get("summary", "").lower()
                op_id = details.get("operationId", "").lower()

                if any(term in summary or term in op_id or term in path.lower()
                       for term in query_lower.split()):
                    return f"""
**{method.upper()} {path}**
Summary: {details.get("summary", "N/A")}
Operation: {details.get("operationId", "N/A")}
"""
        return None

    def _find_wsdl_operation(self, wsdl_name: str, query: str) -> Optional[str]:
        """Find specific WSDL operation matching query"""
        if wsdl_name not in self.wsdl_data:
            return None

        query_lower = query.lower()
        wsdl = self.wsdl_data[wsdl_name]

        for op in wsdl["operations"]:
            op_name_lower = op["name"].lower()
            op_desc_lower = op["description"].lower()

            if any(term in op_name_lower or term in op_desc_lower
                   for term in query_lower.split()):
                return f"""
**{op["name"]}**
Description: {op["description"] or "N/A"}
Input: {op["input"]}
Output: {op["output"]}
"""
        return None

    def list_endpoints(self, api_name: str = None) -> str:
        """List all available endpoints"""
        lines = ["## Available Endpoints
"]

        for doc in self.docs:
            if doc["type"] != "openapi":
                continue
            if api_name and api_name.lower() not in doc["title"].lower():
                continue

            lines.append(f"### {doc['title']}")
            spec = doc.get("raw", {})

            for path, methods in spec.get("paths", {}).items():
                for method, details in methods.items():
                    if method in ["get", "post", "put", "patch", "delete"]:
                        lines.append(f"  {method.upper():6} {path}")
            lines.append("")

        return "
".join(lines)


    def list_wsdl_operations(self, wsdl_name: str = None) -> str:
        """List all operations in WSDL files"""
        lines = ["## WSDL Operations
"]

        if wsdl_name:
            matched = None
            wsdl_name_lower = wsdl_name.lower().replace("_", " ").replace("-", " ")

            for name, data in self.wsdl_data.items():
                name_lower = name.lower().replace("_", " ").replace("-", " ")
                if wsdl_name_lower in name_lower or name_lower in wsdl_name_lower:
                    matched = data
                    break

            if not matched:
                for name, data in self.wsdl_data.items():
                    if wsdl_name.lower() in name.lower():
                        matched = data
                        break

            if matched:
                lines.append(f"### {matched['name']}")
                lines.append(f"Description: {matched['description']}
")
                lines.append("Operations:")
                for op in matched["operations"]:
                    desc = f" - {op['description']}" if op["description"] else ""
                    lines.append(f"  {op['name']}{desc}")
                return "
".join(lines)
            else:
                return f"WSDL '{wsdl_name}' not found. Use --list-wsdl to see available WSDLs."

        lines.append("Available WSDL Services:
")
        for name, data in sorted(self.wsdl_data.items()):
            op_count = len(data["operations"])
            lines.append(f"  {name}: {op_count} operations")

        lines.append(f"
Total: {len(self.wsdl_data)} WSDL files")
        lines.append("
Use --wsdl <name> to see operations for a specific WSDL")

        return "
".join(lines)



def main():
    rebuild = "--rebuild" in sys.argv
    if rebuild:
        sys.argv.remove("--rebuild")

    rag = WorkdayRAG(rebuild_embeddings=rebuild)

    if len(sys.argv) < 2:
        print("Workday RAG - Query your Workday API documentation")
        print("
Usage:")
        print("  python workday_rag.py 'your question'")
        print("  python workday_rag.py --list              # List all REST endpoints")
        print("  python workday_rag.py --list-wsdl         # List all WSDL services")
        print("  python workday_rag.py --wsdl <name>       # Show operations in a WSDL")
        print("  python workday_rag.py --rebuild           # Rebuild embeddings cache")
        print("  python workday_rag.py --interactive       # Interactive mode")
        print("
Examples:")
        print("  python workday_rag.py 'how to create payment term'")
        print("  python workday_rag.py --wsdl Human_Resources")
        print("  python workday_rag.py --rebuild 'authentication headers'")
        print("
Search Mode:")
        if rag.embedding_manager.is_available:
            print("  Semantic search ENABLED (using Gemini embeddings)")
        else:
            print("  Keyword search only (set GEMINI_API_KEY for semantic search)")
        return

    if sys.argv[1] == "--list":
        print(rag.list_endpoints())
    elif sys.argv[1] == "--list-wsdl":
        print(rag.list_wsdl_operations())
    elif sys.argv[1] == "--wsdl":
        if len(sys.argv) < 3:
            print("Usage: python workday_rag.py --wsdl <wsdl_name>")
            print("
Available WSDLs:")
            for name in sorted(rag.wsdl_data.keys()):
                print(f"  {name}")
        else:
            wsdl_name = sys.argv[2]
            print(rag.list_wsdl_operations(wsdl_name))
    elif sys.argv[1] == "--interactive":
        print("Workday RAG Interactive Mode (type 'quit' to exit)")
        search_mode = "semantic" if rag.embedding_manager.is_available else "keyword"
        print(f"Search mode: {search_mode}")
        while True:
            try:
                q = input("
> ").strip()
                if q.lower() in ["quit", "exit", "q"]:
                    break
                if q:
                    print(rag.query(q))
            except (KeyboardInterrupt, EOFError):
                break
    else:
        question = " ".join(sys.argv[1:])
        print(rag.query(question))


if __name__ == "__main__":
    main()
