from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.db import get_session
from app.api.dependencies.permissions import (
    admin_permissions,
    employer_permissions,
    user_permissions,
)
from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserRequest,
    UserResponse,
)
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def add_user(
    request: UserRequest,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    A route to add a user.

    Args:
        request (UserRequest): The request object containing user data.
        session (AsyncSession): The database session.
    Returns:
        UserResponse: The response object containing the added user data.
    """
    service = UserService(session)
    user = await service.add(request)
    return user


@router.get("/")
async def get_users(
    _: UserResponse = Depends(admin_permissions),
    session: AsyncSession = Depends(get_session),
) -> list[UserResponse]:
    """
    A route to get all users.

    Args:
        session (AsyncSession): The database session.
    Returns:
        list[UserResponse]: A list of user response objects.
    """
    service = UserService(session)
    users = await service.get_all()
    return users


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    user: UserResponse = Depends(employer_permissions),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    A route to get a user by id.
    Args:
        user_id (str): The id of the user to be retrieved.
        session (AsyncSession): The database session.
    Returns:
        UserResponse: The response object containing the user data.
    """

    user_permissions(user_id=user_id, user=user)

    service = UserService(session)
    user = await service.get_by_id(user_id)
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    request: UserRequest,
    user: UserResponse = Depends(employer_permissions),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    A route to update a user by id.
    Args:
        user_id (str): The id of the user to be updated.
        request (UserRequest): The request object containing the updated user data.
        session (AsyncSession): The database session.
    Returns:
        UserResponse: The response object containing the updated user data.
    """

    user_permissions(user_id=user_id, user=user)

    service = UserService(session)
    user = await service.update(user_id, request)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    user: UserResponse = Depends(employer_permissions),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    A route to delete a user by id.
    Args:
        user_id (str): The id of the user to be deleted.
        session (AsyncSession): The database session.
    Returns:
        UserResponse: The response object containing the deleted user data.
    """

    user_permissions(user_id=user_id, user=user)

    service = UserService(session)
    user = await service.delete_by_id(user_id)
    return user


@router.post(
    "/login",
    status_code=200,
)
async def login_user(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """
    Endpoint to login a user
    - Args:
        - request: LoginRequest: User login data
        - session: AsyncSession: Database session
    - Returns:
        - TokenResponse: User token data
    """
    service = UserService(session)

    user = await service.login(request)

    return user


@router.post("/token")
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    """

    Endpoint para gerar token de acesso com base na requisição vinda do swagger

    Deve obrigatoriamente ter estes campos

    - access_token: Token de Acesso (Você deve gerar este campo usando os dados que chegaram no forms)

    - token_type: "bearer" # Neste caso o tipo é bearer

    Documentação OFICIAL -> https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#update-the-dependencies

    - Args:
        - form_data: OAuth2PasswordRequestForm:
            - username: str # E-mail
            - password: str
            - client_id: str | None
            - client_secret: str | None
            - scopes: str | None
            - grant_type: str | None

    - Returns:
        dict: {
            "access_token": str,
            "token_type": str
        }

    """
    service = UserService(session)

    login_data = LoginRequest(
        email=form_data.username, password=form_data.password
    )
    token_response = await service.login(login_data)

    response = {
        "access_token": token_response.access_token,
        "token_type": "bearer",
    }

    return response
