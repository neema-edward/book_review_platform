from app import app, db, Author, Book, Review, book_review

def seed():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create authors
        author1 = Author(name='Jane Austen')
        author2 = Author(name='George Orwell')
        db.session.add_all([author1, author2])
        db.session.commit()

        # Create books
        book1 = Book(title='Pride and Prejudice', publication_year=1813, author_id=author1.id)
        book2 = Book(title='Sense and Sensibility', publication_year=1811, author_id=author1.id)
        book3 = Book(title='1984', publication_year=1949, author_id=author2.id)
        book4 = Book(title='Animal Farm', publication_year=1945, author_id=author2.id)
        db.session.add_all([book1, book2, book3, book4])
        db.session.commit()

        # Create reviews
        review1 = Review(rating=5, comment='Amazing romance!')
        review2 = Review(rating=4, comment='Very witty!')
        review3 = Review(rating=5, comment='Dystopian masterpiece!')
        review4 = Review(rating=3, comment='Good but dark.')
        review5 = Review(rating=4, comment='Thought-provoking.')
        review6 = Review(rating=5, comment='Loved the characters!')
        db.session.add_all([review1, review2, review3, review4, review5, review6])
        db.session.commit()

        # Link reviews to books
        book1.reviews = [review1, review2]
        book3.reviews = [review3, review4, review5]
        book4.reviews = [review6]
        db.session.commit()

        print('Database seeded successfully!')

if __name__ == '__main__':
    seed()