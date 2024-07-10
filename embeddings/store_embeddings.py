# embeddings/store_embeddings.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pinecone import Pinecone, Index, ServerlessSpec
from data.fetch_books import fetch_books
from data.preprocess import preprocess_books
from embeddings.generate_embeddings import generate_embeddings
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_NAMESPACE

# def store_embeddings(book_data):
#     pc = Pinecone(api_key=PINECONE_API_KEY)

#     # List all indexes
#     index_list = pc.list_indexes()

#     if PINECONE_INDEX_NAME not in index_list:
#         # Create index if it doesn't exist
#         pc.create_index(
#             name=PINECONE_INDEX_NAME,
#             dimension=384,
#             metric='cosine',
#             spec=ServerlessSpec(
#                 cloud='aws',
#                 region='us-east-1'
#             )
#         )

#     # Access the existing index
#     index = pc.Index(PINECONE_INDEX_NAME)

#     # Generate embeddings
#     embeddings, texts = generate_embeddings(book_data)

#     # Prepare metadata
#     metadatas = [{
#         'title': book['title'],
#         'authors': book['authors'],
#         'description': book['description'],
#         'subject': book['subject']
#     } for book in book_data]

#     # Prepare vectors
#     vectors = [(str(i), embedding, metadata) for i, (embedding, metadata) in enumerate(zip(embeddings, metadatas))]

#     # Upsert vectors to Pinecone
#     index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)
#     print(f"Stored embeddings for {len(texts)} books in Pinecone")

# if __name__ == "__main__":
#     sample_books = fetch_books("love")  # Fetch sample books for the subject "love"
#     processed_books = preprocess_books(sample_books)
#     store_embeddings(processed_books)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pinecone
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_NAMESPACE

def store_embeddings(book_data, embeddings, texts):
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # List all indexes
    index_list = pc.list_indexes()

    # if PINECONE_INDEX_NAME not in index_list:
    #     # Create index if it doesn't exist
    #     pc.create_index(
    #         name=PINECONE_INDEX_NAME,
    #         dimension=384,
    #         metric='cosine',
    #         spec=ServerlessSpec(
    #             cloud='aws',
    #             region='us-east-1'
    #         )
    #     )

    # Access the existing index
    index = pc.Index(PINECONE_INDEX_NAME)

    # Prepare metadata
    metadatas = [{
        'title': book['title'],
        'authors': book['authors'],
        'description': book['description'],
        'subject': book['subject']
    } for book in book_data]

    # Prepare vectors
    vectors = [(str(i), embedding, metadata) for i, (embedding, metadata) in enumerate(zip(embeddings, metadatas))]

    # Upsert vectors to Pinecone
    index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)
    print(f"Stored embeddings for {len(texts)} books in Pinecone")
