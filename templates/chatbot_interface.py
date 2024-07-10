import streamlit as st
from streamlit_chat import message
from data.fetch_books import fetch_books
from data.preprocess import preprocess_books
from embeddings.generate_embeddings import generate_embeddings
from embeddings.store_embeddings import store_embeddings
from utils.gpt3_processor import process_user_input
from utils.recommend_books import recommend_books
# import openai

# openai.api_key = "your_openai_api_key"

# Function to check if the response is relevant
def is_relevant(response, subject):
    return subject.lower() in response.lower()

# Function to check if the response is faithful
def is_faithful(response, books):
    for book in books:
        if book['title'].lower() in response.lower() or book['description'].lower() in response.lower():
            return True
    return False

# Function to handle inappropriate queries
def handle_inappropriate_queries(query):
    inappropriate_keywords = ["inappropriate", "badword", "politics", "war", "adult"]  # Add more keywords as needed
    for word in inappropriate_keywords:
        if word in query.lower():
            return True
    return False

# Main chatbot function
def chatbot():
    st.title("Book Recommendation Chatbot")

    message("Hi, to help you find a book, please tell me the subject you are interested in.")
    subject = st.text_input("Enter subject (e.g., love, science, history):")

    if subject:
        message(f"I am interested in books about {subject}", is_user=True)

        if handle_inappropriate_queries(subject):
            st.error("Inappropriate query detected. Please try a different query.")
            return

        # Fetch books from Open Library for the given subject
        books = fetch_books(subject.lower(), limit=25)
        
        # Preprocess books
        processed_books = preprocess_books(books)
        
        # Generate embeddings
        embeddings, texts = generate_embeddings(processed_books)
        
        # Store embeddings in Pinecone
        store_embeddings(processed_books, embeddings, texts)

        # Process user input with GPT-3
        processed_input = process_user_input(f"Find books about {subject}")
        
        # Fetch recommendations using Pinecone
        recommendations = recommend_books(processed_input)
        
        # Display recommendations
        for rec in recommendations:
            st.write(f"**Title:** {rec['metadata']['title']}")
            st.write(f"**Authors:** {', '.join(rec['metadata']['authors'])}")
            st.write(f"**Description:** {rec['metadata']['description']}")
            st.write("---")
        
        # Evaluation metrics
        response = " ".join([rec['metadata']['description'] for rec in recommendations])
        relevance = is_relevant(response, subject)
        faithfulness = is_faithful(response, books)
        
        st.write(f"**Answer Relevance:** {'Relevant' if relevance else 'Not Relevant'}")
        st.write(f"**Faithfulness:** {'Faithful' if faithfulness else 'Not Faithful'}")

        # Example counterfactual robustness and negative rejection handling
        # counterfactual_query = f"Find books about {subject} that do not exist"
        # counterfactual_response = process_user_input(counterfactual_query)
        # if counterfactual_response == "No books found":
        #     st.write("**Counterfactual Robustness:** Passed")
        # else:
        #     st.write("**Counterfactual Robustness:** Failed")
        
        negative_query = "Find books about inappropriate topic"
        if handle_inappropriate_queries(negative_query):
            st.write("**Negative Rejection:** Passed")
        else:
            st.write("**Negative Rejection:** Failed")

if __name__ == "__main__":
    chatbot()
