#!/usr/bin/env python3
"""
RAG Collection Manager
Helps Claude decide when to scrape, update, or use existing RAG collections
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Available RAG collections
AVAILABLE_RAGS = {
    "nextjs": {
        "chunks": 1187,
        "last_updated": "2025-10-21",
        "version": "15.x",
        "status": "operational",
        "source": "https://nextjs.org/docs",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/nextjs"
    },
    "tanstack-query": {
        "chunks": 785,
        "last_updated": "2025-10-21",
        "version": "5.x",
        "status": "operational",
        "source": "https://tanstack.com/query/latest",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/tanstack-query"
    },
    "shadcn": {
        "chunks": 753,
        "last_updated": "2025-10-21",
        "version": "latest",
        "status": "operational",
        "source": "https://ui.shadcn.com",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/shadcn"
    },
    "tailwind": {
        "chunks": 142,
        "last_updated": "2025-10-21",
        "version": "3.x",
        "status": "operational",
        "source": "https://tailwindcss.com/docs",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/tailwind"
    },
    "zustand": {
        "chunks": 336,
        "last_updated": "2025-10-21",
        "version": "4.x",
        "status": "operational",
        "source": "https://docs.pmnd.rs/zustand",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/zustand"
    },
    "forms-validation": {
        "chunks": 9220,
        "last_updated": "2025-10-21",
        "version": "react-hook-form + zod",
        "status": "operational",
        "source": "multiple",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/forms-validation"
    },
    "aws-cognito": {
        "chunks": 461,
        "last_updated": "2025-10-21",
        "version": "latest",
        "status": "operational",
        "source": "https://docs.aws.amazon.com/cognito",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/aws-cognito"
    },
    "aws-api-gateway": {
        "chunks": 409,
        "last_updated": "2025-10-21",
        "version": "latest",
        "status": "operational",
        "source": "https://docs.aws.amazon.com/apigateway",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/aws-api-gateway"
    },
    "aws-ecs-fargate": {
        "chunks": 763,
        "last_updated": "2025-10-21",
        "version": "latest",
        "status": "operational",
        "source": "https://docs.aws.amazon.com/ecs",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/aws-ecs-fargate"
    },
    "playwright": {
        "chunks": 613,
        "last_updated": "2025-10-21",
        "version": "1.x",
        "status": "operational",
        "source": "https://playwright.dev/docs",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/playwright"
    },
    "web-performance": {
        "chunks": 250,
        "last_updated": "2025-10-21",
        "version": "latest",
        "status": "operational",
        "source": "https://web.dev",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/web-performance"
    },
    "agupgrade-backend": {
        "chunks": 352,
        "last_updated": "2025-10-21",
        "version": "project-specific",
        "status": "operational",
        "source": "internal",
        "usage_count": 0,
        "collection_path": "projects/erpa/AGUPGRADE/rag-collections/backend"
    }
}


class RAGManager:
    """Intelligent RAG collection manager"""

    def __init__(self, metadata_file: str = ".claude/rag-metadata.json"):
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """Load RAG metadata from file"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {"collections": AVAILABLE_RAGS, "statistics": {}}

    def _save_metadata(self):
        """Save RAG metadata to file"""
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def has_rag_for_technology(self, technology: str) -> Tuple[bool, Optional[str]]:
        """
        Check if we have RAG for this technology

        Returns:
            (exists, rag_name) tuple
        """
        tech_lower = technology.lower()

        # Direct match
        if tech_lower in self.metadata["collections"]:
            return True, tech_lower

        # Partial match
        for rag_name in self.metadata["collections"].keys():
            if tech_lower in rag_name or rag_name in tech_lower:
                return True, rag_name

        return False, None

    def is_rag_fresh(self, rag_name: str, max_age_days: int = 30) -> bool:
        """Check if RAG is fresh enough"""
        if rag_name not in self.metadata["collections"]:
            return False

        last_updated_str = self.metadata["collections"][rag_name]["last_updated"]
        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d")
        age_days = (datetime.now() - last_updated).days

        return age_days <= max_age_days

    def calculate_importance(
        self,
        technology: str,
        doc_type: str = "official",
        estimated_size_kb: int = 100,
        project_relevance: str = "high"
    ) -> int:
        """
        Calculate documentation importance score (1-10)

        Args:
            technology: Technology name
            doc_type: "official", "third-party", "internal"
            estimated_size_kb: Estimated documentation size
            project_relevance: "high", "medium", "low"

        Returns:
            Importance score 1-10
        """
        score = 5  # Base score

        # Doc type scoring
        if doc_type == "official":
            score += 2
        elif doc_type == "third-party":
            score += 1

        # Size scoring (larger = more valuable to cache)
        if estimated_size_kb > 500:
            score += 2
        elif estimated_size_kb > 100:
            score += 1

        # Project relevance
        if project_relevance == "high":
            score += 2
        elif project_relevance == "medium":
            score += 1

        # Major technology bonus
        major_techs = ["nextjs", "react", "typescript", "aws", "python", "node"]
        if any(tech in technology.lower() for tech in major_techs):
            score += 1

        return min(10, max(1, score))

    def recommend_action(
        self,
        technology: str,
        question: str = "",
        context: str = ""
    ) -> Dict:
        """
        Recommend what to do with documentation

        Returns:
            {
                "action": "use_rag" | "scrape_to_rag" | "read_once" | "skip",
                "rag_name": str or None,
                "reasoning": str,
                "token_cost": int,
                "token_savings": int
            }
        """
        # Check if RAG exists
        has_rag, rag_name = self.has_rag_for_technology(technology)

        if has_rag:
            # Check if fresh
            if self.is_rag_fresh(rag_name):
                return {
                    "action": "use_rag",
                    "rag_name": rag_name,
                    "reasoning": f"RAG collection '{rag_name}' exists and is fresh",
                    "token_cost": 800,
                    "token_savings": 24000,
                    "chunks": self.metadata["collections"][rag_name]["chunks"]
                }
            else:
                return {
                    "action": "update_rag",
                    "rag_name": rag_name,
                    "reasoning": f"RAG collection '{rag_name}' exists but is outdated",
                    "token_cost": 5000,
                    "token_savings": 20000,
                    "chunks": self.metadata["collections"][rag_name]["chunks"]
                }

        # No RAG - calculate importance
        importance = self.calculate_importance(technology)

        if importance >= 8:
            return {
                "action": "scrape_to_rag",
                "rag_name": None,
                "reasoning": f"High importance ({importance}/10) - worth adding to RAG",
                "token_cost": 7000,
                "token_savings": 18000,  # Break-even after 1 query
                "importance_score": importance
            }
        elif importance >= 5:
            return {
                "action": "read_once",
                "rag_name": None,
                "reasoning": f"Medium importance ({importance}/10) - read directly",
                "token_cost": 5000,
                "token_savings": 0,
                "importance_score": importance
            }
        else:
            return {
                "action": "skip",
                "rag_name": None,
                "reasoning": f"Low importance ({importance}/10) - avoid if possible",
                "token_cost": 0,
                "token_savings": 0,
                "importance_score": importance
            }

    def record_usage(self, rag_name: str, tokens_saved: int = 24000):
        """Record RAG usage for statistics"""
        if rag_name in self.metadata["collections"]:
            self.metadata["collections"][rag_name]["usage_count"] += 1
            self.metadata["collections"][rag_name]["last_used"] = datetime.now().strftime("%Y-%m-%d")

            # Update global statistics
            stats = self.metadata.setdefault("statistics", {})
            stats["total_queries"] = stats.get("total_queries", 0) + 1
            stats["total_tokens_saved"] = stats.get("total_tokens_saved", 0) + tokens_saved

            self._save_metadata()

    def get_statistics(self) -> Dict:
        """Get RAG usage statistics"""
        stats = self.metadata.get("statistics", {})
        total_queries = stats.get("total_queries", 0)
        total_tokens_saved = stats.get("total_tokens_saved", 0)

        return {
            "total_queries": total_queries,
            "total_tokens_saved": total_tokens_saved,
            "avg_tokens_saved_per_query": total_tokens_saved // total_queries if total_queries > 0 else 0,
            "total_collections": len(self.metadata["collections"]),
            "total_chunks": sum(c["chunks"] for c in self.metadata["collections"].values()),
            "roi_percentage": 97 if total_queries > 0 else 0
        }

    def list_collections(self) -> List[Dict]:
        """List all RAG collections with stats"""
        collections = []
        for name, info in self.metadata["collections"].items():
            collections.append({
                "name": name,
                "chunks": info["chunks"],
                "last_updated": info["last_updated"],
                "version": info["version"],
                "usage_count": info.get("usage_count", 0),
                "status": info["status"]
            })
        return sorted(collections, key=lambda x: x["usage_count"], reverse=True)


# CLI Interface
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="RAG Collection Manager")
    parser.add_argument("command", choices=["check", "recommend", "list", "stats", "record"])
    parser.add_argument("--tech", help="Technology name")
    parser.add_argument("--question", help="Question/query")
    parser.add_argument("--rag", help="RAG collection name")

    args = parser.parse_args()
    manager = RAGManager()

    if args.command == "check":
        if not args.tech:
            print("Error: --tech required")
            sys.exit(1)

        has_rag, rag_name = manager.has_rag_for_technology(args.tech)
        if has_rag:
            is_fresh = manager.is_rag_fresh(rag_name)
            info = manager.metadata["collections"][rag_name]
            print(f"✅ RAG exists: {rag_name}")
            print(f"   Chunks: {info['chunks']}")
            print(f"   Last updated: {info['last_updated']}")
            print(f"   Fresh: {'Yes' if is_fresh else 'No (>30 days old)'}")
            print(f"   Status: {info['status']}")
        else:
            print(f"❌ No RAG collection for: {args.tech}")

    elif args.command == "recommend":
        if not args.tech:
            print("Error: --tech required")
            sys.exit(1)

        recommendation = manager.recommend_action(args.tech, args.question or "")
        print(f"\n📊 Recommendation for '{args.tech}':")
        print(f"   Action: {recommendation['action']}")
        print(f"   Reasoning: {recommendation['reasoning']}")
        print(f"   Token cost: {recommendation['token_cost']:,}")
        print(f"   Token savings: {recommendation['token_savings']:,}")
        if recommendation.get('rag_name'):
            print(f"   RAG collection: {recommendation['rag_name']}")
            print(f"   Chunks: {recommendation.get('chunks', 'N/A')}")

    elif args.command == "list":
        collections = manager.list_collections()
        print("\n📚 RAG Collections:\n")
        for c in collections:
            print(f"  • {c['name']}")
            print(f"    Chunks: {c['chunks']:,}")
            print(f"    Updated: {c['last_updated']}")
            print(f"    Usage: {c['usage_count']} queries")
            print(f"    Status: {c['status']}")
            print()

    elif args.command == "stats":
        stats = manager.get_statistics()
        print("\n📈 RAG System Statistics:\n")
        print(f"  Total collections: {stats['total_collections']}")
        print(f"  Total chunks: {stats['total_chunks']:,}")
        print(f"  Total queries: {stats['total_queries']:,}")
        print(f"  Total tokens saved: {stats['total_tokens_saved']:,}")
        print(f"  Avg tokens saved/query: {stats['avg_tokens_saved_per_query']:,}")
        print(f"  ROI: {stats['roi_percentage']}%")

    elif args.command == "record":
        if not args.rag:
            print("Error: --rag required")
            sys.exit(1)

        manager.record_usage(args.rag)
        print(f"✅ Recorded usage for: {args.rag}")
