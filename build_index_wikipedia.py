"""Build Knowledge Graph Index from Wikipedia articles."""
import sys
import os

# Add parent directory to path for both PyCharm and command line
project_root = os.path.dirname(os.path.abspath(__file__))
rag_agent_path = os.path.join(project_root, 'rag_agent')
if rag_agent_path not in sys.path:
    sys.path.insert(0, rag_agent_path)

# Try absolute import first (PyCharm), then relative (command line)
try:
    from rag_agent.src.wikipedia_reader import WikipediaReader
    from rag_agent.src.indexer import KnowledgeGraphIndexer
    from rag_agent.src.config import WIKIPEDIA_LANGUAGE, MAX_ARTICLES
except ImportError:
    from src.wikipedia_reader import WikipediaReader
    from src.indexer import KnowledgeGraphIndexer
    from src.config import WIKIPEDIA_LANGUAGE, MAX_ARTICLES



def build_index(topic: str, max_articles: int = None):
    """
    Build a knowledge graph index from Wikipedia articles on a given topic.
    
    Args:
        topic: Topic to search for on Wikipedia
        max_articles: Maximum number of articles to fetch (uses config default if not specified)
    """
    max_articles = max_articles or MAX_ARTICLES
    
    print(f"\n{'='*60}")
    print(f"Building Knowledge Graph from Wikipedia")
    print(f"Topic: {topic}")
    print(f"Max Articles: {max_articles}")
    print(f"Language: {WIKIPEDIA_LANGUAGE}")
    print(f"{'='*60}\n")
    
    # Initialize Wikipedia reader
    reader = WikipediaReader(language=WIKIPEDIA_LANGUAGE, max_articles=max_articles)
    
    # Fetch articles
    print("Fetching Wikipedia articles...")
    documents = reader.fetch_articles_by_topic(topic, limit=max_articles)
    
    if not documents:
        print("No articles fetched. Exiting.")
        return
    
    print(f"\nFetched {len(documents)} articles:")
    for doc in documents:
        print(f"  - {doc.metadata['title']}")
    
    # Build index
    print("\nBuilding knowledge graph index...")
    indexer = KnowledgeGraphIndexer()
    indexer.build_index(documents)
    
    print("\n" + "="*60)
    print("Knowledge graph built successfully!")
    print(f"Index saved to: {indexer.storage_dir}")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_index_wikipedia.py <topic> [max_articles]")
        print("Example: python build_index_wikipedia.py 'Machine Learning' 15")
        sys.exit(1)
    
    topic = sys.argv[1]
    max_articles = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    build_index(topic, max_articles)
