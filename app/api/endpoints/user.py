from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.db import get_session
from app.schemas.user import UserRequest, UserResponse
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
    service = UserService(session)
    user = await service.get_by_id(user_id)
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    request: UserRequest,
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
    service = UserService(session)
    user = await service.update(user_id, request)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
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
    print("user_id: ", user_id)
    service = UserService(session)
    user = await service.delete_by_id(user_id)
    return user
