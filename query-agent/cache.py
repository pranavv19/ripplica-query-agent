import os
import json
from typing import Optional, List, Dict

CACHE_FILE = "cache.json"

# Load cache from file or initialize empty
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache: List[Dict] = json.load(f)
else:
    cache: List[Dict] = []

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def add_to_cache(query: str, embedding: list, summary: str):
    entry = {
        "query": query.lower(),
        "embedding": embedding,
        "summary": summary
    }
    cache.append(entry)
    save_cache()

def get_cached_summary(query: str) -> Optional[str]:
    q = query.lower()
    for entry in cache:
        if entry["query"] == q:
            return entry["summary"]
    return None

def get_all_embeddings() -> List[list]:
    return [entry["embedding"] for entry in cache]

def get_all_queries() -> List[str]:
    return [entry["query"] for entry in cache]

def get_all_summaries() -> List[str]:
    return [entry["summary"] for entry in cache]

# Example usage
def print_cache():
    for entry in cache:
        print(f"Query: {entry['query']}\nSummary: {entry['summary'][:100]}...\n")

if __name__ == "__main__":
    print("Current cache entries:")
    print_cache()

    # Add a test entry
    try:
        from embedder import get_embedding
        test_query = "What is the capital of France?"
        test_summary = "The capital of France is Paris."
        test_embedding = get_embedding(test_query).tolist()
        add_to_cache(test_query, test_embedding, test_summary)
        print("\nAdded test entry.")
    except Exception as e:
        print(f"[Error] Could not add test entry: {e}")

    print("\nCache after adding test entry:")
    print_cache()

    # Retrieve summary
    found = get_cached_summary(test_query)
    print("\nRetrieved summary for test query:", found)

    # List all queries and embeddings
    print("\nAll queries:", get_all_queries())
    print("All embeddings (first only):", get_all_embeddings()[:1]) 