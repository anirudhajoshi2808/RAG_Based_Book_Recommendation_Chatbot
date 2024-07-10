import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.fetch_books import fetch_books
from data.preprocess import preprocess_books
from langchain_huggingface import HuggingFaceEmbeddings

def generate_embeddings(processed_books):
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    texts = [book['description'] for book in processed_books]
    embeddings = model.embed_documents(texts)
    print(f"Generated embeddings for {len(embeddings)} books")
    return embeddings, texts


