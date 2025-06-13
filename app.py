from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, ma, Author, Book, Review, book_schema, books_schema
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Welcome to the Book Review Platform!'

# GET /books: List all books with author and reviews
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.join(Author).all()
    return jsonify(books_schema.dump(books))

# GET /books/<id>: Get a specific book
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book_schema.dump(book))

# POST /books: Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or not all(key in data for key in ['title', 'publication_year', 'author_id']):
        return jsonify({'error': 'Missing required fields'}), 400
    if not Author.query.get(data['author_id']):
        return jsonify({'error': 'Author not found'}), 404
    book = Book(
        title=data['title'],
        publication_year=data['publication_year'],
        author_id=data['author_id']
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book_schema.dump(book)), 201

# PATCH /books/<id>: Update a book
@app.route('/books/<int:id>', methods=['PATCH'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    book.title = data.get('title', book.title)
    book.publication_year = data.get('publication_year', book.publication_year)
    db.session.commit()
    return jsonify(book_schema.dump(book))

# DELETE /books/<id>: Delete a book and its reviews
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

# /scrape: Scrape book data from Open Library API
@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        response = requests.get('http://openlibrary.org/search.json?q=python')
        data = response.json()
        books_added = 0
        authors_added = 0

        for item in data.get('docs', [])[:2]:  # Limit to 2 books for simplicity
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

        return jsonify({
            'books_added': books_added,
            'authors_added': authors_added
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)