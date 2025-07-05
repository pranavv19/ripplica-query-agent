# Ripplica Query Agent

This backend is a modular Python pipeline for classifying queries, scraping the web, summarizing results, and caching answers using semantic and LLM-based matching. **There is currently NO REST API or server—usage is via the command line only.**

## Features

- Query classification (Gemini)
- Web scraping (Playwright, DuckDuckGo)
- Summarization (Gemini)
- Semantic deduplication (FAISS, LLM)
- Caching
- Command-line interface (CLI)

---

## Demo


[Watch the demo video](https://drive.google.com/file/d/1RlmeMWbsKVlCwQemyf5gw0SCpRzjzuqV/view?usp=sharing)

## Setup

1. **Enter the backend directory:**
   ```sh
   cd query-agent-backend
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Install Playwright browser binaries:**
   ```sh
   playwright install
   ```

4. **(Optional) Set up your `.env` file:**
   - Create a `.env` file with your Gemini API key:
     ```env
     GEMINI_API_KEY=your-key-here
     ```

---

## Usage (Command Line)

Run the main pipeline interactively:
```sh
python main.py
```
- You will be prompted to enter a query.
- The pipeline will classify, check cache, scrape, summarize, and cache the result.
- Output is printed to the terminal.

---

## Project Structure

- `main.py` — Orchestrates the full pipeline (CLI entry point)
- `classify.py` — Classifies queries using Gemini
- `scraper.py` — Web scraping with Playwright (sync API)
- `summarizer.py` — Summarizes text/pages using Gemini
- `embedder.py` — Embedding via sentence-transformers
- `vector_store.py` — FAISS vector search for semantic deduplication
- `llm_semantic_match.py` — LLM-based semantic match for cache
- `cache.py` — JSON-based cache for queries, embeddings, and summaries
- `requirements.txt` — Python dependencies

---

## Troubleshooting
- **Playwright errors on Windows:**
  - Make sure you use the sync API (already set up).
  - If you see subprocess or event loop errors, restart your terminal and ensure you are not running inside Jupyter or Anaconda Prompt.
- **Protobuf errors:**
  - Run `pip install protobuf==3.20.3` to fix TensorFlow/protobuf compatibility issues.
- **No browser found:**
  - Run `playwright install` again.

---

