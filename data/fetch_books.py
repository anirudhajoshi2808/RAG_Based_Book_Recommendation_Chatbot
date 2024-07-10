import requests

# def fetch_books(subject):
#     url = f"https://openlibrary.org/subjects/{subject}.json?details=false"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         books = data.get('works', [])
#         print(f"Fetched {len(books)} books for subject: {subject}")
#         return books
#     else:
#         print(f"Failed to fetch books for subject: {subject}, status code: {response.status_code}")
#         return []

def fetch_books(subject, limit=25):
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{subject}&maxResults={limit}"
    response = requests.get(url)
    books = response.json().get('items', [])
    fetched_books = []
    for book in books:
        volume_info = book.get('volumeInfo', {})
        fetched_books.append({
            'title': volume_info.get('title', 'No Title'),
            'authors': volume_info.get('authors', ['Unknown Author']),
            'description': volume_info.get('description', ''),
            'subject': subject
        })
    return fetched_books


