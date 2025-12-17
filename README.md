
# Knowledge Graph RAG POC

A Retrieval-Augmented Generation (RAG) system that builds a knowledge graph from Wikipedia articles and allows you to query it using natural language.

## Overview

This project fetches real-world articles from Wikipedia, builds a Knowledge Graph using **LlamaIndex**, and queries it using the **Mistral** LLM (locally via **Ollama**).

## Features

- ✅ Fetch real Wikipedia articles via MediaWiki API
- ✅ Build knowledge graph index using LlamaIndex
- ✅ Query using Mistral LLM (via Ollama)
- ✅ Local embeddings with HuggingFace
- ✅ Source attribution using Wikipedia URLs

## Quick Start

### 1. Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) with `mistral` model installed:
  ```bash
  ollama run mistral
  ```

### 2. Setup

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Usage

The project uses a single CLI entry point: `rag_agent/main.py`.

#### Build a Knowledge Graph
Fetch articles on a specific topic and build the index.

```bash
# Syntax: python rag_agent/main.py --index --topic "Your Topic" [--limit N]

python rag_agent/main.py --index --topic "Artificial Intelligence" --limit 10
```

#### Query the Knowledge Graph
Ask questions based on the indexed content.

```bash
# Single query
python rag_agent/main.py --query "What is deep learning?"

# Interactive mode
python rag_agent/main.py --interactive
```

## Project Structure

- `rag_agent/`: Core source code
  - `src/wikipedia_reader.py`: Fetches articles from Wikipedia
  - `src/indexer.py`: Builds the Knowledge Graph
  - `src/query.py`: Handles LLM queries
- `storage`/`: Generated vector indices (gitignored)

## Troubleshooting

- **Ollama Connection Error**: Ensure Ollama is running (`ollama serve` or `ollama run mistral`).
- **No Documents Found**: Try a broader topic name for the Wikipedia search.
