from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from datetime import datetime

# Create a base class for declarative models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def password(self):
        """Property method to prevent reading the password directly."""
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = bcrypt.hash(password.encode('utf8'))

    def verify_password(self, password):
        """
        Verify if the provided password matches the hashed password stored in the database.

        :param password: The password to verify.
        :return: True if the password matches, False otherwise.
        """
        return bcrypt.verify(password, self.password_hash)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship('Book', back_populates='author')

    @property
    def num_books(self):
        """Get the number of books associated with this author."""
        return len(self.books)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    pages = Column(Integer, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship('Author', back_populates='books')
