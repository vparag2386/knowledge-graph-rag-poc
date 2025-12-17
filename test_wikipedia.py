"""Test Wikipedia Reader and Query Engine."""
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
    from rag_agent.src.query import QueryEngine
except ImportError:
    from src.wikipedia_reader import WikipediaReader
    from src.indexer import KnowledgeGraphIndexer
    from src.query import QueryEngine



def test_wikipedia_fetch():
    """Test fetching Wikipedia articles."""
    print("\n" + "="*60)
    print("Testing Wikipedia Article Fetching")
    print("="*60 + "\n")
    
    # Initialize reader
    reader = WikipediaReader(language="en", max_articles=5)
    
    # Test search
    topic = "Artificial Intelligence"
    print(f"Searching for articles about: {topic}\n")
    
    # Fetch articles
    documents = reader.fetch_articles_by_topic(topic, limit=5)
    
    print(f"\n{'='*60}")
    print(f"Fetched {len(documents)} articles:")
    print("="*60)
    
    for i, doc in enumerate(documents, 1):
        title = doc.metadata['title']
        url = doc.metadata['url']
        summary = doc.metadata['summary'][:200]
        content_len = len(doc.text)
        
        # Handle Unicode encoding for console output
        print(f"\n{i}. {title}")
        print(f"   URL: {url}")
        print(f"   Summary: {summary.encode('ascii', 'ignore').decode('ascii')}...")
        print(f"   Content length: {content_len} characters")



def test_knowledge_graph():
    """Test building and querying the knowledge graph."""
    print("\n" + "="*60)
    print("Testing Knowledge Graph Building and Querying")
    print("="*60 + "\n")
    
    # Fetch articles
    reader = WikipediaReader(language="en", max_articles=5)
    topic = "Machine Learning"
    print(f"Fetching articles about: {topic}")
    documents = reader.fetch_articles_by_topic(topic, limit=5)
    
    if not documents:
        print("No articles fetched. Cannot build index.")
        return
    
    # Build index
    print("\nBuilding knowledge graph index...")
    indexer = KnowledgeGraphIndexer()
    indexer.build_index(documents)
    
    # Initialize query engine
    print("\nInitializing query engine...")
    query_engine = QueryEngine()
    query_engine.initialize()
    
    # Test queries
    queries = [
        "What is machine learning?",
        "What are the types of machine learning?",
        "Explain supervised learning",
        "What is the difference between AI and machine learning?"
    ]
    
    print("\n" + "="*60)
    print("Testing Queries")
    print("="*60)
    
    for query in queries:
        print(f"\n{'─'*60}")
        print(f"Q: {query}")
        print(f"{'─'*60}")
        response = query_engine.query(query)
        print(f"A: {response}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        # Test full knowledge graph with queries
        test_knowledge_graph()
    else:
        # Just test fetching
        test_wikipedia_fetch()
        
        print("\n" + "="*60)
        print("To test the full knowledge graph with queries, run:")
        print("  python test_wikipedia.py query")
        print("="*60)
