#!/usr/bin/env python3
"""
Index Documentation into Vector Store
Standalone script to index markdown files for semantic search
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# LangChain imports
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.docstore.document import Document

BASE_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude")
VECTOR_STORE_PATH = BASE_PATH / "unified-memory/vector-store/global"
DOCUMENTS_PATH = BASE_PATH / "documents"

def get_embeddings():
    """Get FREE HuggingFace embeddings"""
    print("🔄 Loading HuggingFace embeddings (FREE)...")
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✅ Embeddings loaded successfully (384 dimensions)")
    return embeddings

def load_documents_from_folder(folder_path: Path):
    """Load all markdown and text files from a folder"""
    print(f"\n📂 Loading documents from: {folder_path}")

    documents = []

    # Load markdown files
    md_files = list(folder_path.glob("*.md"))
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                doc = Document(
                    page_content=content,
                    metadata={
                        'source': str(md_file),
                        'filename': md_file.name,
                        'type': 'markdown',
                        'folder': folder_path.name
                    }
                )
                documents.append(doc)
                print(f"  ✅ Loaded: {md_file.name}")
        except Exception as e:
            print(f"  ❌ Error loading {md_file.name}: {e}")

    # Load text files
    txt_files = list(folder_path.glob("*.txt"))
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
                doc = Document(
                    page_content=content,
                    metadata={
                        'source': str(txt_file),
                        'filename': txt_file.name,
                        'type': 'text',
                        'folder': folder_path.name
                    }
                )
                documents.append(doc)
                print(f"  ✅ Loaded: {txt_file.name}")
        except Exception as e:
            print(f"  ❌ Error loading {txt_file.name}: {e}")

    print(f"📊 Total documents loaded: {len(documents)}")
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

def index_documents(folders_to_index):
    """Index documents from specified folders"""
    print("="*60)
    print("📚 DOCUMENT INDEXING")
    print("="*60)
    print(f"Vector Store: {VECTOR_STORE_PATH}")
    print(f"Folders to index: {', '.join([f.name for f in folders_to_index])}")

    # Load embeddings
    embeddings = get_embeddings()

    # Collect all documents
    all_documents = []
    for folder in folders_to_index:
        docs = load_documents_from_folder(folder)
        all_documents.extend(docs)

    if not all_documents:
        print("\n⚠️  No documents found to index")
        return

    print(f"\n📊 Total documents to process: {len(all_documents)}")

    # Chunk documents
    chunks = chunk_documents(all_documents)

    # Create or load vector store
    print(f"\n🔄 Creating vector store at: {VECTOR_STORE_PATH}")
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)

    # Check if vector store already exists
    if (VECTOR_STORE_PATH / "chroma.sqlite3").exists():
        print("📂 Existing vector store found - adding new documents...")
        vector_store = Chroma(
            persist_directory=str(VECTOR_STORE_PATH),
            embedding_function=embeddings
        )
        vector_store.add_documents(chunks)
    else:
        print("📂 Creating new vector store...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(VECTOR_STORE_PATH)
        )

    print("✅ Vector store created/updated successfully")

    # Summary
    print("\n" + "="*60)
    print("📊 INDEXING SUMMARY")
    print("="*60)
    print(f"Documents processed: {len(all_documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Vector store location: {VECTOR_STORE_PATH}")
    print(f"Status: ✅ Ready for semantic search")

    return vector_store

def test_search(vector_store, query="Claude Desktop setup"):
    """Test semantic search"""
    print("\n" + "="*60)
    print("🔍 TESTING SEMANTIC SEARCH")
    print("="*60)
    print(f"Query: {query}")

    results = vector_store.similarity_search(query, k=3)

    print(f"\n📊 Found {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"  Source: {result.metadata.get('filename', 'unknown')}")
        print(f"  Folder: {result.metadata.get('folder', 'unknown')}")
        print(f"  Preview: {result.page_content[:200]}...")
        print()

def main():
    """Main indexing workflow"""
    import argparse
    parser = argparse.ArgumentParser(description='Index documentation for semantic search')
    parser.add_argument('--test', action='store_true', help='Test search after indexing')
    parser.add_argument('--query', type=str, default='Claude Desktop setup', help='Test query')
    args = parser.parse_args()

    try:
        # Define folders to index
        folders_to_index = [
            DOCUMENTS_PATH / "setup",
            DOCUMENTS_PATH / "reports",
            DOCUMENTS_PATH / "reference"
        ]

        # Verify folders exist
        folders_to_index = [f for f in folders_to_index if f.exists()]

        if not folders_to_index:
            print("❌ No valid folders found to index")
            return

        # Index documents
        vector_store = index_documents(folders_to_index)

        # Test search if requested
        if args.test and vector_store:
            test_search(vector_store, args.query)

        print("\n✅ Indexing complete!")
        print("\n💡 Your documents are now searchable via Claude Desktop:")
        print("   Example: 'Search for memory migration guide'")

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
