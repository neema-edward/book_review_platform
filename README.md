# 📚 Book Review Platform

A Flask-based web application to manage books, authors, and reviews, including data scraping from the Open Library API.

---

## 🚀 Features

- CRUD operations for books
- Relationships between books, authors, and reviews
- Scrape book data from Open Library API
- JSON API using Flask-Marshmallow
- SQLite database with Flask-Migrate

---

## 🛠️ Tech Stack

- Python 3.12+
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Marshmallow
- Marshmallow-SQLAlchemy
- Requests
- SQLite (via SQLAlchemy)

---

## 📦 Setup Instructions (using Pipenv)

## 1. Clone the Repository
  git clone <your-repo-url>
  cd book_review_platform


## 2. Install Dependencies
  pipenv install
  pipenv install flask flask-sqlalchemy flask-marshmallow flask-migrate requests
  pipenv install marshmallow==3.20.1 flask-marshmallow==0.14.0 marshmallow-sqlalchemy==0.29.0


## 3. Activate the Virtual Environment
  bash
  Copy
  Edit
  pipenv shell

## 4. Set Up the Database
  bash
  Copy
  Edit
  export FLASK_APP=app.py  # On Windows, use: set FLASK_APP=app.py
  flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade

## 5. Run the App
  bash
  Copy
  Edit
  flask run --port=8080
  Visit: http://localhost:8080

## 📘 API Endpoints
  Method	Route	Description
  GET	/	Welcome message
  GET	/books	List all books with authors/reviews
  GET	/books/<id>	Get a specific book
  POST	/books	Create a new book
  PATCH	/books/<id>	Update a book
  DELETE	/books/<id>	Delete a book
  GET	/scrape	Scrape book data from Open Library

## 📝 Example POST /books Request
json
Copy
Edit
{
  "title": "Flask for Beginners",
  "publication_year": 2022,
  "author_id": 1
}
