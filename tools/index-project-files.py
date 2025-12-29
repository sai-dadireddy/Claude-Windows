#!/usr/bin/env python3
"""
Index Project Files into Vector Store
Indexes .claude-project.md, CLAUDE.md, and project documentation for cross-project search
"""

import sys
import os
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# LangChain imports
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

BASE_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude")
VECTOR_STORE_PATH = BASE_PATH / "unified-memory/vector-store/global"

# Exclude patterns
EXCLUDE_DIRS = {'node_modules', 'backups', '.git', '__pycache__', 'dist', 'build'}

def get_embeddings():
    """Get FREE HuggingFace embeddings"""
    print("🔄 Loading HuggingFace embeddings (FREE)...")
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✅ Embeddings loaded successfully")
    return embeddings

def should_exclude_path(path: Path) -> bool:
    """Check if path should be excluded"""
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

def find_project_files():
    """Find all project configuration and documentation files"""
    print("="*60)
    print("🔍 SCANNING FOR PROJECT FILES")
    print("="*60)

    project_files = {
        'claude_project_md': [],
        'claude_md': [],
        'readme': []
    }

    # Find .claude-project.md files
    print("\n📋 Finding .claude-project.md files...")
    for md_file in BASE_PATH.glob("**/.claude-project.md"):
        if not should_exclude_path(md_file):
            project_files['claude_project_md'].append(md_file)
            print(f"  ✅ Found: {md_file.relative_to(BASE_PATH)}")

    # Find CLAUDE.md files (case-insensitive)
    print("\n📋 Finding CLAUDE.md files...")
    for md_file in BASE_PATH.glob("**/CLAUDE.md"):
        if not should_exclude_path(md_file):
            project_files['claude_md'].append(md_file)
            print(f"  ✅ Found: {md_file.relative_to(BASE_PATH)}")

    # Also check lowercase
    for md_file in BASE_PATH.glob("**/claude.md"):
        if not should_exclude_path(md_file) and md_file not in project_files['claude_md']:
            # Only add if not a duplicate (case-insensitive file system)
            if not any(f.resolve() == md_file.resolve() for f in project_files['claude_md']):
                project_files['claude_md'].append(md_file)
                print(f"  ✅ Found: {md_file.relative_to(BASE_PATH)}")

    # Find README.md in project folders (not in node_modules)
    print("\n📋 Finding project README.md files...")
    projects_dir = BASE_PATH / "claude/projects"
    if projects_dir.exists():
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir() and project_dir.name not in EXCLUDE_DIRS:
                readme = project_dir / "README.md"
                if readme.exists():
                    project_files['readme'].append(readme)
                    print(f"  ✅ Found: {readme.relative_to(BASE_PATH)}")

    # Summary
    print("\n" + "="*60)
    print("📊 FILES FOUND")
    print("="*60)
    print(f".claude-project.md: {len(project_files['claude_project_md'])}")
    print(f"CLAUDE.md: {len(project_files['claude_md'])}")
    print(f"README.md: {len(project_files['readme'])}")
    print(f"Total: {sum(len(v) for v in project_files.values())}")

    return project_files

def load_project_files(project_files):
    """Load project files into documents"""
    print("\n" + "="*60)
    print("📂 LOADING PROJECT FILES")
    print("="*60)

    documents = []

    # Load .claude-project.md files
    for file_path in project_files['claude_project_md']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Extract project name from path
                if 'projects' in file_path.parts:
                    idx = file_path.parts.index('projects')
                    if idx + 1 < len(file_path.parts):
                        project_name = file_path.parts[idx + 1]
                    else:
                        project_name = file_path.parent.name
                else:
                    project_name = file_path.parent.name

                doc = Document(
                    page_content=content,
                    metadata={
                        'source': str(file_path),
                        'filename': file_path.name,
                        'type': 'claude_project',
                        'project': project_name,
                        'category': 'project_config'
                    }
                )
                documents.append(doc)
                print(f"✅ Loaded: {project_name}/.claude-project.md")
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")

    # Load CLAUDE.md files
    for file_path in project_files['claude_md']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Extract project name
                if 'projects' in file_path.parts:
                    idx = file_path.parts.index('projects')
                    if idx + 1 < len(file_path.parts):
                        project_name = file_path.parts[idx + 1]
                    else:
                        project_name = file_path.parent.name
                else:
                    project_name = file_path.parent.name

                doc = Document(
                    page_content=content,
                    metadata={
                        'source': str(file_path),
                        'filename': file_path.name,
                        'type': 'claude_instructions',
                        'project': project_name,
                        'category': 'project_config'
                    }
                )
                documents.append(doc)
                print(f"✅ Loaded: {project_name}/CLAUDE.md")
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")

    # Load README.md files
    for file_path in project_files['readme']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                project_name = file_path.parent.name

                doc = Document(
                    page_content=content,
                    metadata={
                        'source': str(file_path),
                        'filename': file_path.name,
                        'type': 'readme',
                        'project': project_name,
                        'category': 'project_docs'
                    }
                )
                documents.append(doc)
                print(f"✅ Loaded: {project_name}/README.md")
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")

    print(f"\n📊 Total documents loaded: {len(documents)}")
    return documents

def chunk_documents(documents):
    """Split documents into chunks for embedding"""
    print(f"\n✂️  Chunking {len(documents)} documents...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    return chunks

def index_project_files(project_files):
    """Index project files into vector store"""
    print("\n" + "="*60)
    print("📚 INDEXING PROJECT FILES")
    print("="*60)

    # Load embeddings
    embeddings = get_embeddings()

    # Load documents
    documents = load_project_files(project_files)

    if not documents:
        print("\n⚠️  No documents to index")
        return None

    # Chunk documents
    chunks = chunk_documents(documents)

    # Load existing vector store and add new documents
    print(f"\n🔄 Adding to existing vector store at: {VECTOR_STORE_PATH}")

    try:
        # Load existing store
        vector_store = Chroma(
            persist_directory=str(VECTOR_STORE_PATH),
            embedding_function=embeddings
        )

        # Add new documents
        vector_store.add_documents(chunks)
        print("✅ Project files added to vector store")
    except Exception as e:
        print(f"❌ Error adding to vector store: {e}")
        return None

    # Summary
    print("\n" + "="*60)
    print("📊 INDEXING SUMMARY")
    print("="*60)
    print(f"Project files indexed: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Vector store location: {VECTOR_STORE_PATH}")
    print(f"Status: ✅ Ready for cross-project search")

    return vector_store

def test_cross_project_search(vector_store):
    """Test cross-project semantic search"""
    print("\n" + "="*60)
    print("🔍 TESTING CROSS-PROJECT SEARCH")
    print("="*60)

    test_queries = [
        "How to configure nginx for Angular projects",
        "What projects use AWS Lambda",
        "Memory management configuration"
    ]

    for query in test_queries:
        print(f"\n📊 Query: '{query}'")
        results = vector_store.similarity_search(query, k=3)

        if results:
            for i, result in enumerate(results, 1):
                project = result.metadata.get('project', 'unknown')
                doc_type = result.metadata.get('type', 'unknown')
                print(f"  Result {i}: {project} ({doc_type})")
                print(f"    Preview: {result.page_content[:150]}...")
        else:
            print("  No results found")

def main():
    """Main workflow"""
    try:
        # Find project files
        project_files = find_project_files()

        total_files = sum(len(v) for v in project_files.values())
        if total_files == 0:
            print("\n⚠️  No project files found to index")
            return

        # Index files
        vector_store = index_project_files(project_files)

        # Test search
        if vector_store:
            test_cross_project_search(vector_store)

        print("\n✅ Project indexing complete!")
        print("\n💡 You can now search across all projects in Claude Desktop:")
        print("   Example: 'Search for nginx configuration patterns'")
        print("   Example: 'Find projects using AWS services'")

    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
