"""Query Engine for the Knowledge Graph."""
from .indexer import KnowledgeGraphIndexer


from llama_index.core import Settings
from llama_index.core.llms import ChatMessage, MessageRole

class QueryEngine:
    """Handles queries against the Knowledge Graph with chat memory."""
    
    def __init__(self):
        self.indexer = KnowledgeGraphIndexer()
        self.query_engine = None
        self.chat_history = []
    
    def initialize(self):
        """Initialize the query engine."""
        index = self.indexer.get_index()
        self.query_engine = index.as_query_engine(
            similarity_top_k=3,
            response_mode="tree_summarize",
            streaming=True  # Enable streaming by default
        )
        print("Query engine initialized")
    
    def condense_question(self, question: str) -> str:
        """Rewrite question based on chat history."""
        if not self.chat_history:
            return question
            
        # Create context string from history
        history_str = "\n".join([
            f"{msg.role}: {msg.content}" 
            for msg in self.chat_history[-4:]  # Keep last 2 turns
        ])
        
        prompt = (
            "Given the following conversation history and a follow-up question, "
            "rephrase the follow-up question to be a standalone question.\n\n"
            f"Chat History:\n{history_str}\n\n"
            f"Follow Up Input: {question}\n"
            "Standalone question:"
        )
        
        response = Settings.llm.complete(prompt)
        return str(response).strip()

    def query(self, question: str) -> str:
        """Query the knowledge graph (non-streaming)."""
        if self.query_engine is None:
            self.initialize()
            
        # Rewrite question if needed
        standalone_question = self.condense_question(question)
        if standalone_question != question:
            print(f"\nRewritten Query: {standalone_question}")
        else:
            print(f"\nQuery: {question}")
            
        response = self.query_engine.query(standalone_question)
        
        # Update history
        self.chat_history.append(ChatMessage(role=MessageRole.USER, content=question))
        self.chat_history.append(ChatMessage(role=MessageRole.ASSISTANT, content=str(response)))
        
        return str(response)

    def query_stream(self, question: str):
        """Query the knowledge graph with streaming response."""
        if self.query_engine is None:
            self.initialize()
            
        # Rewrite question if needed
        standalone_question = self.condense_question(question)
        if standalone_question != question:
            print(f"\nRewritten Query: {standalone_question}")
        else:
            print(f"\nQuery: {question}")
            
        response = self.query_engine.query(standalone_question)
        
        # Update history (we'll append the full response after streaming in the caller, 
        # but for simplicity we can't easily do it here without consuming the stream.
        # So we'll return the response object and let the caller handle history update if needed,
        # or we can accumulate here. Let's accumulate here.)
        
        full_response = ""
        for token in response.response_gen:
            full_response += token
            yield token
            
        # Update history
        self.chat_history.append(ChatMessage(role=MessageRole.USER, content=question))
        self.chat_history.append(ChatMessage(role=MessageRole.ASSISTANT, content=full_response))

