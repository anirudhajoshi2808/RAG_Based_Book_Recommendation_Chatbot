import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pinecone
from sentence_transformers import SentenceTransformer
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_NAMESPACE, PINECONE_HOST

def recommend_books(query):
    # Initialize Pinecone
    pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

    # Access the existing index
    index = pc.Index(PINECONE_INDEX_NAME)

    # Initialize HuggingFace embeddings model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode(query).tolist()

    # Perform similarity search
    response = index.query(
        vector=[query_embedding],
        top_k=3,
        include_metadata=True,
        namespace=PINECONE_NAMESPACE
    )

    # Extract recommendations
    recommendations = response['matches']
    return recommendations


