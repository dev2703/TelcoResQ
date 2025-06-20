import faiss
import numpy as np
import os
from telcoresq.config import settings

def create_faiss_index(embeddings):
    """
    Creates a FAISS index from a list of embeddings.
    """
    if not embeddings:
        return None
    
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index

def save_faiss_index(index, path=settings.VECTOR_STORE_PATH):
    """
    Saves a FAISS index to a file.
    """
    if index is None:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)
    print(f"FAISS index saved to {path}")

def load_faiss_index(path=settings.VECTOR_STORE_PATH):
    """
    Loads a FAISS index from a file.
    """
    if not os.path.exists(path):
        return None
    return faiss.read_index(path) 