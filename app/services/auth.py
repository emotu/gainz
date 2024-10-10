from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel, Field, computed_field
from app.config import settings
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class DummyUser(BaseModel):
    id: str
    username: str


class LoginForm(BaseModel):
    username: str


class RegistrationForm(BaseModel):
    name: str
    username: str
    password: str


class AuthToken(BaseModel):
    """model to hold and validate jwt user claim"""
    uid: str
    username: str
    # iss: str = settings.JWT_ISSUER_CLAIM
    exp: datetime = Field(default_factory=lambda: datetime.now() + timedelta(hours=settings.JWT_EXPIRES_IN_HOURS))
    token_type: str = "bearer"

    @computed_field
    @property
    def access_token(self) -> bytes:
        """ Generate the JWT using the data from the model object"""
        data = dict(sub=self.uid, username=self.username, exp=self.exp)
        return jwt.encode(data, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM).encode("utf-8")

    @classmethod
    def get_user_id(cls, token) -> str | None:
        """ Parse the token, and extract the uid"""
        data = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        validated = cls.model_validate(data)
        return validated.uid


async def authenticate_user(username: str, password: str) -> User | bool:
    """ Authenticate a user with given username and password """
    user = await User.check_user_exists(username)
    if not user or not user.check_password(password):
        return False
    return user


async def get_user_from_token(token: str) -> User | DummyUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

    except InvalidTokenError:
        raise credentials_exception

    user_id = payload.get("sub")
    user = DummyUser(id=user_id, username=payload.get("username"))

    # user = await User.get(user_id)
    # if not user:
    #     raise credentials_exception

    return user


async def get_authenticated_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Dependency function to check that a user is authenticated before attempting to execute the request endpoint.
    It validates the authorization header to determine if a user has successfully logged in.

    This dependency is designed to not return any parameters and so, can be used as a route dependency.
    """

    return await get_user_from_token(token)


async def get_current_user(current_user: Annotated[User, Security(get_authenticated_user)]):
    """ Dependency function to check that a user is authenticated before attempting to execute the request endpoint."""
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive or invalid user")
    return current_user
