# Wikipedia RAG Knowledge Graph

A RAG (Retrieval-Augmented Generation) system that builds a knowledge graph from real-world Wikipedia articles and allows you to query it using natural language.

## Features

- ✅ Fetch real Wikipedia articles via MediaWiki API
- ✅ Build knowledge graph index using LlamaIndex
- ✅ Query using Mistral LLM (via Ollama)
- ✅ Local embeddings with HuggingFace
- ✅ Source attribution with Wikipedia URLs

## Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install required packages (if not already installed)
pip install -r requirements.txt
```

### 2. Ensure Ollama is Running

Make sure Ollama is running with the Mistral model:

```bash
ollama run mistral
```

### 3. Test Wikipedia Fetching

```bash
python test_wikipedia.py
```

This will fetch 5 Wikipedia articles about "Artificial Intelligence" and display their summaries.

### 4. Build a Knowledge Graph

```bash
# Build index from Wikipedia articles on any topic
python build_index_wikipedia.py "Machine Learning" 10
```

This will:
- Search Wikipedia for "Machine Learning"
- Fetch the top 10 related articles
- Build a vector index knowledge graph
- Save it to `./storage` directory

### 5. Query the Knowledge Graph

```bash
python query_wikipedia.py
```

Then ask questions like:
- "What is machine learning?"
- "Explain supervised learning"
- "What are neural networks?"

## Usage Examples

### Fetch Articles on Different Topics

```bash
# AI and Technology
python build_index_wikipedia.py "Artificial Intelligence" 15
python build_index_wikipedia.py "Quantum Computing" 8
python build_index_wikipedia.py "Blockchain" 10

# Science
python build_index_wikipedia.py "Quantum Physics" 12
python build_index_wikipedia.py "Climate Change" 10

# History
python build_index_wikipedia.py "World War II" 15
python build_index_wikipedia.py "Ancient Rome" 10
```

### Test Full Knowledge Graph

```bash
# This will fetch articles, build index, and run sample queries
python test_wikipedia.py query
```

## Configuration

Edit `rag_agent/.env` or `rag_agent/src/config.py` to customize:

```python
# Wikipedia settings
WIKIPEDIA_LANGUAGE = "en"  # Language code
MAX_ARTICLES = 10          # Max articles per topic
READER_TYPE = "wikipedia"  # "wikijs" or "wikipedia"

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"
```

## How It Works

1. **WikipediaReader** fetches articles from Wikipedia using the MediaWiki API
2. **KnowledgeGraphIndexer** converts articles to embeddings and builds a vector index
3. **QueryEngine** uses the index to find relevant content and generates answers using Mistral LLM

## Files

- `rag_agent/src/wikipedia_reader.py` - Wikipedia article fetcher
- `rag_agent/src/indexer.py` - Knowledge graph builder
- `rag_agent/src/query.py` - Query engine
- `test_wikipedia.py` - Test script
- `build_index_wikipedia.py` - Build index from Wikipedia
- `query_wikipedia.py` - Interactive query interface

## Switching Between Wiki.js and Wikipedia

To use the original Wiki.js source:

1. Update `config.py`: `READER_TYPE = "wikijs"`
2. Ensure Wiki.js is running and `WIKI_API_KEY` is set
3. Use the original scripts with `WikiReader` instead of `WikipediaReader`

## Requirements

- Python 3.8+
- Ollama with Mistral model
- Internet connection (for Wikipedia API)
- ~2GB disk space (for embeddings model)

## Troubleshooting

**Unicode encoding errors**: Fixed in the latest version with ASCII encoding for console output

**Ollama not running**: Start Ollama with `ollama run mistral`

**No index found**: Build an index first with `build_index_wikipedia.py`

**Slow first run**: The HuggingFace embedding model downloads on first use (~400MB)
