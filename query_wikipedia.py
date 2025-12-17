"""Interactive Query Interface for Wikipedia-based Knowledge Graph."""
import sys
import os

# Add parent directory to path for both PyCharm and command line
project_root = os.path.dirname(os.path.abspath(__file__))
rag_agent_path = os.path.join(project_root, 'rag_agent')
if rag_agent_path not in sys.path:
    sys.path.insert(0, rag_agent_path)

# Try absolute import first (PyCharm), then relative (command line)
try:
    from rag_agent.src.query import QueryEngine
except ImportError:
    from src.query import QueryEngine



def main():
    """Run interactive query interface."""
    print("\n" + "="*60)
    print("Wikipedia Knowledge Graph - Interactive Query Interface")
    print("="*60)
    print("\nInitializing query engine...")
    
    try:
        query_engine = QueryEngine()
        query_engine.initialize()
        
        print("\nQuery engine ready!")
        print("Type 'exit' or 'quit' to stop.\n")
        
        while True:
            query = input("\nYour question: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            if query.lower() in ['clear', 'reset']:
                query_engine.chat_history = []
                print("\n[Chat history cleared]")
                continue
            
            if not query:
                continue
            
            print(f"\n{'-'*60}")
            print("Answer: ", end="", flush=True)
            
            # Use streaming query
            for token in query_engine.query_stream(query):
                print(token, end="", flush=True)
                
            print(f"\n{'-'*60}")
    
    except FileNotFoundError:
        print("\n[X] No index found!")
        print("Please build the index first using:")
        print("  python build_index_wikipedia.py 'Your Topic'")
        print("\nExample:")
        print("  python build_index_wikipedia.py 'Machine Learning' 10")
    
    except Exception as e:
        print(f"\n[X] Error: {e}")


if __name__ == "__main__":
    main()
