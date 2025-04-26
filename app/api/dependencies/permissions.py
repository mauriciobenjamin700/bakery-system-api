from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.db import get_session
from app.api.dependencies.tokens import oauth_access
from app.core.constants.enums.user import UserRoles
from app.core.constants.messages import ERROR_ACCESS_USER_UNAUTHORIZED
from app.core.errors import UnauthorizedError
from app.core.security.tokens import TokenManager
from app.schemas.user import TokenData, UserResponse
from app.services.user import UserService


async def employer_permission(
    token: str = Depends(oauth_access),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Check if the user has CLIENT permissions to access the resource.

    Args:
        token (str): JWT access token.
        session (AsyncSession): Database session.
    Returns:
        UserResponse: User data.
    """

    payload = TokenManager.verify_token(token)

    token_data = TokenData(**payload)

    service = UserService(session)

    user = await service.get_by_id(token_data.user_id)

    return user


def user_permission(user_id: str, user: UserResponse) -> None:
    """
    Function to Check if the user has user permissions to access the resource. User can only access your resources. Like your account and your data.

    Args:
        user_id (str): User ID to check permissions.
        user (UserResponse): User data.

    Returns:
        None

    Raises:
        UnauthorizedError: If the user does not have permission to access the resource.
    """

    if user.role not in [UserRoles.USER.value, UserRoles.ADMIN.value]:
        raise UnauthorizedError(detail=ERROR_ACCESS_USER_UNAUTHORIZED)

    if user.role.value != UserRoles.ADMIN.value:

        if user.id != user_id:
            raise UnauthorizedError(detail=ERROR_ACCESS_USER_UNAUTHORIZED)

    return user


async def admin_permission(
    token: str = Depends(oauth_access),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    Check if the user has client permissions to access the resource.

    Args:
        token (str): JWT access token.
        session (AsyncSession): Database session.

    Returns:
        UserResponse: User data.
    """

    payload = TokenManager.verify_token(token)

    token_data = TokenData(**payload)

    service = UserService(session)

    user = await service.get_by_id(token_data.user_id)

    if user.role != UserRoles.ADMIN.value:
        raise UnauthorizedError(detail=ERROR_ACCESS_USER_UNAUTHORIZED)

    return user
