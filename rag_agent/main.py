"""Main CLI entry point for RAG Agent."""
import argparse
import sys
from src.reader import WikiReader
from src.indexer import KnowledgeGraphIndexer
from src.query import QueryEngine


def index_wiki():
    """Fetch pages from Wiki.js and build the index."""
    print("=== Indexing Wiki.js Content ===")
    
    # Fetch pages
    reader = WikiReader()
    documents = reader.fetch_all_pages()
    
    if not documents:
        print("No documents found. Exiting.")
        return
    
    # Build index
    indexer = KnowledgeGraphIndexer()
    indexer.build_index(documents)
    
    print("\n[SUCCESS] Indexing complete!")


def query_wiki(question: str):
    """Query the indexed knowledge."""
    print("=== Querying Knowledge Graph ===")
    
    engine = QueryEngine()
    answer = engine.query(question)
    
    print(f"\nAnswer:\n{answer}\n")


def interactive_mode():
    """Interactive query mode."""
    print("=== Interactive Query Mode ===")
    print("Type 'exit' to quit\n")
    
    engine = QueryEngine()
    engine.initialize()
    
    while True:
        question = input("Question: ").strip()
        if question.lower() in ['exit', 'quit', 'q']:
            break
        
        if not question:
            continue
        
        answer = engine.query(question)
        print(f"\nAnswer:\n{answer}\n")


def main():
    parser = argparse.ArgumentParser(description="RAG Agent for Wiki.js")
    parser.add_argument("--index", action="store_true", help="Index Wiki.js content")
    parser.add_argument("--query", type=str, help="Query the knowledge graph")
    parser.add_argument("--interactive", action="store_true", help="Interactive query mode")
    
    args = parser.parse_args()
    
    if args.index:
        index_wiki()
    elif args.query:
        query_wiki(args.query)
    elif args.interactive:
        interactive_mode()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
