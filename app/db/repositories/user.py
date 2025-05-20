from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants.enums.user import UserRoles
from app.core.constants.messages import (
    ERROR_DATABASE_USER_ALREADY_EXISTS,
    ERROR_DATABASE_USER_NOT_FOUND,
    ERROR_REQUIRED_FIELD_ID,
)
from app.core.errors import ConflictError, NotFoundError, ValidationError
from app.db.models import UserModel
from app.schemas.user import UserRequest, UserResponse


class UserRepository:
    """
    User Repository Class to handle all database operations related to User

    - Attributes:
        - db_session: AsyncSession

    - Methods:
        - add: Add a new User to the database
        - get: Get a User from the database
        - update: Update a User in the database
        - delete: Delete a User from the database
    """

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def add(self, model: UserModel) -> UserModel:
        """
        Add a new User to the database

        - Args:
            - model: UserModel

        - Returns:
            - UserModel
        """

        try:
            self.db_session.add(model)
            await self.db_session.commit()
            await self.db_session.refresh(model)
            return model

        except Exception as e:
            print("USER REPOSITORY ADD ERROR: ", e)
            await self.db_session.rollback()
            raise ConflictError(ERROR_DATABASE_USER_ALREADY_EXISTS)

    async def get(
        self,
        id: str | None = None,
        email: str | None = None,
        all_results: bool = False,
    ) -> None | UserModel | Sequence[UserModel]:
        """
        Get a User from the database by id or email. If all_results is True, return all results found in the database.

        - Args:
            - id: str = None
            - email: str = None
            - all_results: bool = False

        - Returns:
            - UserModel
            - List[UserModel]
        """
        if id:
            stmt = select(UserModel).where(UserModel.id == id)
        elif email:
            stmt = select(UserModel).where(UserModel.email == email)
        else:
            stmt = select(UserModel)

        result = await self.db_session.execute(stmt)

        if all_results:
            return result.scalars().all()

        return result.scalars().first()

    async def update(self, model: UserModel) -> UserModel:
        """
        Update a User in the database

        - Args:
            - model: UserModel

        - Returns:
            - UserModel
        """
        await self.db_session.commit()
        await self.db_session.refresh(model)
        return model

    async def delete(
        self, model: UserModel | None = None, id: str | None = None
    ) -> None:
        """
        Delete a User from the database. If model is provided, delete the model. If id is provided, delete the model with the id.

        - Args:
            - model: UserModel : User model to delete
            - id: str : Id of the User model to delete

        - Returns:
            - None
        """
        if model:
            await self.db_session.delete(model)
            await self.db_session.commit()
        elif id:
            stmt = delete(UserModel).where(UserModel.id == id)
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()

            if result.rowcount == 0:
                raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        else:
            raise ValidationError("id", ERROR_REQUIRED_FIELD_ID)

    @staticmethod
    def map_request_to_model(request: UserRequest) -> UserModel:
        """
        A method to map a user request to a user model.

        - Args:
            - request: UserRequest : A user request object.

        - Returns:
            - model: UserModel : A user model object.
        """
        model = UserModel(
            **request.to_dict(include={"role": UserRoles.USER.value})
        )

        return model

    @staticmethod
    def map_model_to_response(model: UserModel) -> UserResponse:
        """
        A method to map a user model to a user response.

        - Args:
            - model: UserModel : A user model object.

        - Returns:
            - response: UserResponse : A user response object.
        """
        response = UserResponse(**model.to_dict(exclude=["password"]))

        return response
