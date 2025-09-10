from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)  # unique=True helps at DB level
    phone_number = db.Column(db.String)

    posts = db.relationship('Post', backref='author')

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author must have a name")
        
        # Check if name already exists
        existing = Author.query.filter(Author.name == value).first()
        if existing:
            raise ValueError("Author name must be unique")
        
        return value

    @validates('phone_number')
    def validate_phone(self, key, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits")
        return value



class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    category = db.Column(db.String)

    # author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    # author = db.relationship('Author', back_populates='posts')
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_words):
            raise ValueError("Title must be clickbait-y (contain: 'Won't Believe', 'Secret', 'Top', or 'Guess')")
        return title
