"""Main CLI entry point for RAG Agent."""
import argparse
from src.wikipedia_reader import WikipediaReader
from src.indexer import KnowledgeGraphIndexer
from src.query import QueryEngine
from src.config import MAX_ARTICLES


def index_wikipedia(topic: str, limit: int = MAX_ARTICLES):
    """Fetch pages from Wikipedia and build the index."""
    print(f"=== Indexing Wikipedia Content: {topic} ===")
    
    # Fetch pages
    reader = WikipediaReader()
    documents = reader.fetch_articles_by_topic(topic, limit=limit)
    
    if not documents:
        print("No documents found. Exiting.")
        return
    
    # Build index
    indexer = KnowledgeGraphIndexer()
    indexer.build_index(documents)
    
    print("\n[SUCCESS] Indexing complete!")


def query_knowledge_graph(question: str):
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
    parser = argparse.ArgumentParser(description="Knowledge Graph RAG Agent (Wikipedia Source)")
    
    # Create mutually exclusive group for modes
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--index", action="store_true", help="Index content from Wikipedia")
    group.add_argument("--query", type=str, help="Query the knowledge graph")
    group.add_argument("--interactive", action="store_true", help="Interactive query mode")

    # Arguments for indexing
    parser.add_argument("--topic", type=str, help="Topic to search on Wikipedia (required for --index)")
    parser.add_argument("--limit", type=int, default=MAX_ARTICLES, help="Max articles to fetch")
    
    args = parser.parse_args()
    
    if args.index:
        if not args.topic:
            print("Error: --topic is required when using --index")
            return
        index_wikipedia(args.topic, args.limit)
    elif args.query:
        query_knowledge_graph(args.query)
    elif args.interactive:
        interactive_mode()


if __name__ == "__main__":
    main()
