from pydantic import BaseModel
from typing import List
import datetime


# Authentication schemas

class TokenSchema(BaseModel):
    """
    Represents a token schema, including the access token and token type.
    """
    access_token: str
    token_type: str


class TokenPayloadSchema(BaseModel):
    """
    Represents a token payload schema, including the username.
    """
    username: str


class UserSchema(BaseModel):
    """
    Represents a user schema, including user details.
    """
    id: int
    username: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInDBSchema(UserSchema):
    """
    Represents a user schema including the password hash, typically used in the database.
    """
    password: str


# Book schema

class BookBaseSchema(BaseModel):
    """
    Represents the base schema for a book, including title and pages.
    """
    title: str
    pages: int


class BookCreateSchema(BookBaseSchema):
    """
    Represents a schema for creating a new book, including author_id.
    """
    author_id: int


class BookEditSchema(BookBaseSchema):
    """
    Represents a schema for editing a book, currently empty.
    """
    pass


class BookSchema(BookBaseSchema):
    """
    Represents a book schema, including its unique id.
    """
    id: int

    class Config:
        orm_mode = True


# Author schema

class AuthorBaseSchema(BaseModel):
    """
    Represents the base schema for an author, including their name.
    """
    name: str


class AuthorCreateSchema(AuthorBaseSchema):
    """
    Represents a schema for creating a new author, currently empty.
    """
    pass


class AuthorSchema(AuthorBaseSchema):
    """
    Represents an author schema, including their unique id, number of books, and a list of books.
    """
    id: int
    num_books: int
    books: List[BookSchema]

    class Config:
        orm_mode = True


class AuthorsResponseSchema(BaseModel):
    """
    Represents a response schema containing a list of authors.
    """
    authors: List[AuthorSchema]


class AuthorResponseSchema(AuthorBaseSchema):
    """
    Represents an author response schema, including their unique id and number of books.
    """
    id: int
    num_books: int

    class Config:
        orm_mode = True


class BookResponseSchema(BookBaseSchema):
    """
    Represents a book response schema, including its unique id, author_id, and an author response schema.
    """
    id: int
    author_id: int
    author: AuthorResponseSchema

    class Config:
        orm_mode = True


class BooksSchema(BaseModel):
    """
    Represents a schema containing a list of book response schemas.
    """
    books: List[BookResponseSchema]
