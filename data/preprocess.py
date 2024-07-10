# from fetch_books import fetch_books
def preprocess_books(book_data):
    processed_data = []
    for book in book_data:
        if 'description' not in book or not book['description']:
            book['description'] = book['title']

        if 'authors' in book:
            authors = [author.get('name', 'Unknown Author') if isinstance(author, dict) else author for author in book['authors']]
        else:
            authors = ['Unknown Author']

        processed_book = {
            'title': book['title'],
            'authors': authors,
            'description': book['description'],
            'subject': book.get('subject', [])
        }
        processed_data.append(processed_book)
    print(f"Processed {len(processed_data)} books")
    return processed_data


