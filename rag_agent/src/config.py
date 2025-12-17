"""Configuration loader for RAG Agent."""
import os
from dotenv import load_dotenv

load_dotenv()

WIKI_URL = os.getenv("WIKI_URL", "http://localhost:3000")
WIKI_API_KEY = os.getenv("WIKI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
STORAGE_DIR = "./storage"

# Wikipedia configuration
WIKIPEDIA_LANGUAGE = os.getenv("WIKIPEDIA_LANGUAGE", "en")
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", "10"))
READER_TYPE = os.getenv("READER_TYPE", "wikipedia")  # "wikijs" or "wikipedia"
