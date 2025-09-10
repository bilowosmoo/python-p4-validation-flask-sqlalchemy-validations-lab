from models import db, Author, Post
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    author = Author(name="John Doe", phone_number="1234567890")
    db.session.add(author)
    db.session.commit()

    post = Post(
        title="Top 10 Secrets You Won't Believe",
        content="x" * 300,  # >= 250 chars
        summary="This is a short summary.",
        category="Fiction",
        author=author
    )
    db.session.add(post)
    db.session.commit()
