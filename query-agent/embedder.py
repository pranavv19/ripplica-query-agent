from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> np.ndarray:
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding 