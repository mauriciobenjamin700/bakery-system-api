from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants.enums.user import UserRoles
from app.core.security.password import hash_password
from app.db.models import UserModel

base = {
    "name": "John Doe",
    "phone": "(89) 91111-2222",
    "email": "jhon.doe@gmail.com",
    "password": hash_password("SafePassword123@"),
    "role": UserRoles.USER.value,
}


async def mock_user_employer_on_db(
    mock_db_session: AsyncSession,
):
    """
    Fixture to create a user on the database.
    """

    data = base.copy()

    user = UserModel(**data)
    session: AsyncSession = mock_db_session

    session.add(user)
    await session.commit()

    return user


def mock_user_employer_login():
    """
    Fixture to create a user on the database.
    """
    return {"email": "jhon.doe@gmail.com", "password": "SafePassword123@"}


async def mock_user_admin_on_db(mock_db_session: AsyncSession):

    data = base.copy()
    data["role"] = UserRoles.ADMIN.value
    data["name"] = "Admin User"
    data["email"] = "email@admin.com"
    user = UserModel(**data)
    session: AsyncSession = mock_db_session

    session.add(user)
    await session.commit()

    return user


def mock_user_admin_login():
    """
    Fixture to create a user on the database.
    """
    return {"email": "email@admin.com", "password": "SafePassword123@"}
