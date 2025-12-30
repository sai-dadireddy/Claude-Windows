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
PDF_AVAILABLE = False
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    pass
try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
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
            # Load PDFs if PyMuPDF available
            if PDF_AVAILABLE:
                for f in PRIVATE_DIR.glob("*.pdf"):
                    try:
                        doc = fitz.open(f)
                        text = ""
                        for page in doc:
                            text += page.get_text()[:5000]
                            if len(text) > 50000: break
                        doc.close()
                        title = f.stem.replace("-", " ").replace("_", " ").title()
                        self.docs.append({"type": "pdf", "file": f.name, "title": title, "content": text[:50000]})
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
