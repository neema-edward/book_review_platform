from app import app, db, Author, Book
import requests

def scrape_books():
    with app.app_context():
        response = requests.get('http://openlibrary.org/search.json?q=python')
        data = response.json()
        books_added = 0
        authors_added = 0

        for item in data.get('docs', [])[:2]:
            author_name = item.get('author_name', ['Unknown'])[0]
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()
                authors_added += 1

            book = Book.query.filter_by(title=item.get('title', '')).first()
            if not book:
                book = Book(
                    title=item.get('title', 'Unknown'),
                    publication_year=item.get('first_publish_year', 2020),
                    author_id=author.id
                )
                db.session.add(book)
                db.session.commit()
                books_added += 1

        print(f'Scraped {books_added} books and {authors_added} authors')

if __name__ == '__main__':
    scrape_books()