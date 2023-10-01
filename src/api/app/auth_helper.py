from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import token_utils
from .database_config import get_db_session
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_by_username(username):
    """
    Retrieve a user from the database based on their username.

    :param username: The username of the user to retrieve.
    :return: The user object if found, None otherwise.
    """
    db: Session = next(get_db_session())
    return db.query(User).filter(User.username == username).first()


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current authenticated user based on the provided access token.

    :param token: The access token used for authentication.
    :return: The authenticated user if the token is valid, raises HTTPException otherwise.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = token_utils.decode_access_token(token)
    if not token_data:
        raise credentials_exception
    user = get_user_by_username(token_data.username)
    if not user:
        raise credentials_exception
    return user
