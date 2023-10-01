from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from .database_config import JWT_SECRET_KEY
from .schemas import TokenPayloadSchema

# Define the algorithm used for JWT
ALGORITHM = "HS256"

# Define the expiration time for access tokens in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token based on the provided data.

    :param data: A dictionary containing data to be encoded into the token.
    :param expires_delta: Optional timedelta for token expiration. If None, default expiration is used.
    :return: Encoded access token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decode an access token and return the token payload.

    :param token: The access token to decode.
    :return: TokenPayloadSchema if decoding is successful, None otherwise.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayloadSchema(**payload)
    except JWTError:
        return None
    return token_data
