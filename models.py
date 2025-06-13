from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# Association table for Book-Review many-to-many relationship
book_review = db.Table('book_review',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('review.id'), primary_key=True)
)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def _repr_(self):
        return f"Author('{self.name}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    reviews = db.relationship('Review', secondary=book_review, backref='books', lazy=True)

    def _repr_(self):
        return f"Book('{self.title}', {self.publication_year})"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)

    def _repr_(self):
        return f"Review({self.rating}, '{self.comment}')"

# Serialization schemas
class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True
    author = ma.Nested('AuthorSchema', only=('name',))
    reviews = ma.Nested('ReviewSchema', many=True)

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
    books = ma.Nested('BookSchema', many=True)

# Initialize schemas
review_schema = ReviewSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)
author_schema = AuthorSchema()