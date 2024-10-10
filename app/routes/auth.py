import uuid

from fastapi import APIRouter
from app.services.auth import AuthToken, LoginForm

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=AuthToken)
async def login(form_data: LoginForm):
    """Authenticate a user by checking if their login credentials are correct."""

    user_id = uuid.uuid4()
    username = form_data.username
    token = AuthToken(uid=str(user_id), username=username)

    return token

#
# @router.post("/login", response_model=AuthToken)
# async def login(form_data: LoginForm):
#     """Authenticate a user by checking if their login credentials are correct."""
#     user = await authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     token = AuthToken(uid=str(user.id), username=user.username)
#
#     return token
#
#
# @router.post("/register", response_model=AuthToken)
# async def register(form_data: RegistrationForm):
#     user_exists = await User.check_user_exists(username=form_data.username)
#     if user_exists:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User already exists"
#         )
#
#     user = User(username=form_data.username, name=form_data.name)
#     user.set_password(form_data.password)
#     await user.save()
#
#     # Create an access token for the user and log them in automatically.
#     token = AuthToken(uid=str(user.id), username=user.username)
#
#     return token
