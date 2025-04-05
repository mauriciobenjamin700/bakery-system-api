from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants.enums.user import UserRoles
from app.core.constants.messages import ERROR_DATABASE_USER_NOT_FOUND, ERROR_DATABASE_USERS_NOT_FOUND, MESSAGE_USER_DELETE_SUCCESS
from app.core.errors import NotFoundError
from app.core.security.password import hash_password
from app.db.models import UserModel
from app.db.repositories.user import UserRepository
from app.schemas.message import Message
from app.schemas.user import (
    UserRequest,
    UserResponse
)


class UserService:
    """
    A service class to handle user operations.

    - Args:
      - db_session: AsyncSession : A database session object.

    - Attributes:
      - repository: UserRepository : A repository object to handle database operations for the user.
    - Methods:
      - add: Add a user to the database.
      - get_by_id: Get a user by id.
      - get_all: Get all users from the database.
      - update: Update a user in the database.
      - delete: Delete a user from the database.
      - map_request_to_model: Map a user request to a user model.
      - map_model_to_response: Map a user model to a user response.

    """
    def __init__(self, db_session: AsyncSession):
        self.repository = UserRepository(db_session)


    async def add(self, request: UserRequest) -> UserResponse:
        """
        A method to add a user to the database.

        - Args:
            - request: UserRequest : A user request object.

        - Returns:
            - response: UserResponse : A user response object
        """

        request.password = hash_password(request.password)

        model = self.map_request_to_model(request)

        model = await self.repository.add(model)

        response = self.map_model_to_response(model)

        return response


    async def get_by_id(self, user_id: str) -> UserResponse:
        """
        A method to get a user by id.

        - Args:
          - user_id: str : A user id.
        - Returns:
          - response: UserResponse : A user response object with the user data.
        """

        model = await self.repository.get(id=user_id)

        if not model:

            raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        response = self.map_model_to_response(model)

        return response


    async def get_all(self) -> list[UserResponse]:
        """
        Get all users from the database.

        - Args:
            - None
        - Returns:
            - response: List[UserResponse] : A list of user response objects.
        """
        models = await self.repository.get(all_results=True)

        if not models or not isinstance(models, list):

            raise NotFoundError(ERROR_DATABASE_USERS_NOT_FOUND)

        response = [self.map_model_to_response(model) for model in models]

        return response

    async def update(self, id: str, request: UserRequest):

        model = await self.repository.get(id=id)

        if not model:

            raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        for key, value in request.to_dict().items():
            if key == "password":
                setattr(model, key, hash_password(value))
            else:
                setattr(model, key, value)

        model = await self.repository.update(model)

        response = self.map_model_to_response(model)

        return response

    async def delete_by_id(self, id: str) -> Message:
        """
        Delete a user from the database by id.

        - Args:
          - id: str : A user id.
        - Returns:
          - Message : A message object with the result of the operation.
        """

        await self.repository.delete(id=id)

        return Message(detail=MESSAGE_USER_DELETE_SUCCESS)


    @classmethod
    def map_request_to_model(cls, request: UserRequest) -> UserModel:
        """
        A method to map a user request to a user model.

        - Args:
            - request: UserRequest : A user request object.

        - Returns:
            - model: UserModel : A user model object.
        """
        model = UserModel(
            **request.to_dict(
                include={
                    "role": UserRoles.USER.value
                }
            )
        )

        return model


    @classmethod
    def map_model_to_response(cls, model: UserModel) -> UserResponse:
        """
        A method to map a user model to a user response.

        - Args:
            - model: UserModel : A user model object.

        - Returns:
            - response: UserResponse : A user response object.
        """
        response = UserResponse(
            **model.to_dict(
                exclude=[
                    "password"
                ]
            )
        )

        return response
