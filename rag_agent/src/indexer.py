"""Knowledge Graph Indexer using LlamaIndex and Ollama."""
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from typing import List
from llama_index.core import Document
import os
from .config import OLLAMA_BASE_URL, OLLAMA_MODEL, STORAGE_DIR


class KnowledgeGraphIndexer:
    """Builds and manages the Knowledge Graph index."""
    
    def __init__(self):
        # Initialize Ollama LLM
        self.llm = Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            request_timeout=120.0
        )
        
        # Initialize local embedding model
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        # Set global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 1024
        Settings.chunk_overlap = 50
        
        self.storage_dir = STORAGE_DIR
        self.index = None
    
    def build_index(self, documents: List[Document]):
        """Build the vector index from documents."""
        print(f"Building index from {len(documents)} documents...")
        
        # Create vector store index
        self.index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True
        )
        
        # Persist to disk
        self.index.storage_context.persist(persist_dir=self.storage_dir)
        print(f"Index built and saved to {self.storage_dir}")
    
    def load_index(self):
        """Load existing index from disk."""
        if not os.path.exists(self.storage_dir):
            raise FileNotFoundError(f"No index found at {self.storage_dir}")
        
        print(f"Loading index from {self.storage_dir}...")
        storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
        self.index = load_index_from_storage(storage_context)
        print("Index loaded successfully")
    
    def get_index(self):
        """Get the current index."""
        if self.index is None:
            try:
                self.load_index()
            except FileNotFoundError:
                raise Exception("No index available. Please build the index first.")
        return self.index
