from sqlalchemy.orm import Session
from .database_config import get_db_session
from .models import User, Book, Author


# Method to seed the database with test data
def seed_data(db: Session):
    # Create a test user
    user = User(username="admin", password="Webster301#")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create test authors
    author1 = Author(name="John Doe")
    db.add(author1)
    db.commit()
    db.refresh(author1)

    author2 = Author(name="Jane Smith")
    db.add(author2)
    db.commit()
    db.refresh(author2)

    # Create test books associated with authors
    book1 = Book(title="The Great Gatsby", pages=218, author_id=author1.id)
    db.add(book1)
    db.commit()
    db.refresh(book1)

    book2 = Book(title="To Kill a Mockingbird", pages=281, author_id=author1.id)
    db.add(book2)
    db.commit()
    db.refresh(book2)

    book3 = Book(title="Pride and Prejudice", pages=279, author_id=author2.id)
    db.add(book3)
    db.commit()
    db.refresh(book3)

    # Add more test authors and books
    author3 = Author(name="Mark Johnson")
    db.add(author3)
    db.commit()
    db.refresh(author3)

    book4 = Book(title="The Catcher in the Rye", pages=224, author_id=author3.id)
    db.add(book4)
    db.commit()
    db.refresh(book4)

    book5 = Book(title="1984", pages=328, author_id=author3.id)
    db.add(book5)
    db.commit()
    db.refresh(book5)

    book6 = Book(title="Brave New World", pages=326, author_id=author3.id)
    db.add(book6)
    db.commit()
    db.refresh(book6)


# Get a database session using 'get_db_session'
db = next(get_db_session())

# Seed the data by calling the 'seed_data' method
seed_data(db)
