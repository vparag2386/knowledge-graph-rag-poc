# Knowledge Graph RAG POC

A Retrieval-Augmented Generation (RAG) system that leverages knowledge graphs to index and query information from real-world sources like Wikipedia and Wiki.js.

## Overview

This project demonstrates how to build a Knowledge Graph using LlamaIndex and query it using the Mistral LLM (via Ollama). It supports fetching data from:
- **Wikipedia**: Real-time article fetching.
- **Wiki.js**: Local documentation knowledge base.

## Quick Start

### 1. Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) with `mistral` model installed (`ollama run mistral`)

### 2. Setup

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Usage

This project contains two main modules.

#### Wikipedia RAG
For detailed instructions on using the Wikipedia RAG agent, please refer to [README_WIKIPEDIA.md](README_WIKIPEDIA.md).

**Quick Example:**
```bash
# 1. Fetch articles and build index
python build_index_wikipedia.py "Artificial Intelligence" 10

# 2. Query the graph
python query_wikipedia.py
```

#### Wiki.js Integration
To use with a local Wiki.js instance:
1. Configure your `.env` file (see `rag_agent/.env`).
2. Run `populate_wiki.py` to seed data if needed.
3. Update `config.py` to use `wikijs` reader.

## Project Structure

- `rag_agent/`: Core RAG logic, indexers, and readers.
- `storage`/`: Generated vector indices and graph stores (ignored by git).
- `*.py`: Utility scripts for building indices and querying.
