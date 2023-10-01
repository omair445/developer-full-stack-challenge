from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta

from .. import schemas
from ..database_config import get_db_session, SECRET_KEY
from ..models import User
from ..token_utils import create_access_token

# Create a FastAPI router for authentication-related routes
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Define constants for token expiration and algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 15
ALGORITHM = "HS256"

# Create a CryptContext for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create an OAuth2 password bearer scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(username: str, password: str, db: Session):
    """
    Authenticate a user based on their username and password.

    :param username: The username of the user to authenticate.
    :param password: The password provided by the user.
    :param db: A SQLAlchemy database session.
    :return: The authenticated user if successful.
    :raises HTTPException: If authentication fails, an HTTP 401 Unauthorized error is raised.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/login", response_model=schemas.TokenSchema)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db_session),
):
    """
    Log in and generate an access token for a user.

    :param form_data: OAuth2PasswordRequestForm containing the username and password.
    :param db: A SQLAlchemy database session.
    :return: A TokenSchema containing the access token.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
