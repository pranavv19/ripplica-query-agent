import faiss
import numpy as np
import os
import json
from embedder import get_embedding

# Constants
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output size
FAISS_INDEX_FILE = "index.faiss"
METADATA_FILE = "metadata.json"
SIMILARITY_THRESHOLD = 0.85 

# Initialize index
if os.path.exists(FAISS_INDEX_FILE):
    index = faiss.read_index(FAISS_INDEX_FILE)
else:
    index = faiss.IndexFlatIP(EMBEDDING_DIM)

if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)
else:
    metadata = []

def add_to_store(query: str, summary: str):
    query_lc = query.lower()
    vec = get_embedding(query_lc).astype("float32")
    index.add(np.array([vec]))
    metadata.append({"query": query_lc, "summary": summary})
    persist()

def check_similarity(query: str) -> str | None:
    query_lc = query.lower()
    vec = get_embedding(query_lc).astype("float32")
    D, I = index.search(np.array([vec]), k=1)

    if D[0][0] >= SIMILARITY_THRESHOLD:
        return metadata[I[0][0]]["summary"]
    return None

def persist():
    faiss.write_index(index, FAISS_INDEX_FILE)
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)
