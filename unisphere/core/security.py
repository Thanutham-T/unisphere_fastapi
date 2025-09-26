import datetime

from jose import jwt

from . import config

ALGORITHM = "HS256"

settings = config.get_settings()


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    """
    Create a JWT access token.

    The token will include the provided payload data, a subject (`sub`) claim,
    and an expiration time. If `expires_delta` is not provided, a default
    expiration is used from the application settings.

    Args:
        data (dict): The payload to encode into the JWT. Should include a 'sub' key for the user ID.
        expires_delta (datetime.timedelta | None): Optional expiration duration. 
                                                   Defaults to settings.access_token_expire_minutes.

    Returns:
        str: The encoded JWT access token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(
            tz=datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "sub": str(data.get("sub", 0))})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict, expires_delta: datetime.timedelta | None = None
) -> str:
    """
    Create a JWT refresh token.

    The token includes the provided payload data and an expiration time.
    Unlike the access token, it does not include a `sub` claim.

    Args:
        data (dict): The payload to encode into the JWT.
        expires_delta (datetime.timedelta | None): Optional expiration duration. 
                                                   Defaults to settings.access_token_expire_minutes.

    Returns:
        str: The encoded JWT refresh token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(
            tz=datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
