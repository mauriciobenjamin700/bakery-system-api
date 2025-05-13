from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants.messages import (
    ERROR_DATABASE_USER_NOT_FOUND,
    ERROR_DATABASE_USERS_NOT_FOUND,
    ERROR_TOKEN_REQUIRED,
    MESSAGE_USER_DELETE_SUCCESS,
)
from app.core.errors import NotFoundError, ValidationError
from app.core.generate.passwords import generate_random_password
from app.core.security.password import hash_password, verify_password
from app.core.security.tokens import TokenManager
from app.db.repositories.user import UserRepository
from app.schemas.message import Message
from app.schemas.user import (
    LoginRequest,
    TokenData,
    TokenResponse,
    UserRequest,
    UserResponse,
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

        model = self.repository.map_request_to_model(request)

        model = await self.repository.add(model)

        response = self.repository.map_model_to_response(model)

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

        response = self.repository.map_model_to_response(model)

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

        response = [
            self.repository.map_model_to_response(model) for model in models
        ]

        return response

    async def update(self, id: str, request: UserRequest):
        """
        Update a user in the database.

        Args
            id (str): The id of the user to update.
            request (UserRequest): The user request object containing the updated data.
        Returns
            UserResponse: The updated user response object.
        """
        model = await self.repository.get(id=id)

        if not model:

            raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        for key, value in request.to_dict().items():
            if key == "password":
                setattr(model, key, hash_password(value))
            else:
                setattr(model, key, value)

        model = await self.repository.update(model)

        response = self.repository.map_model_to_response(model)

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

    async def login(self, request: LoginRequest) -> TokenResponse:
        """
        A method to login a user.

        - Args:
          - request: UserRequest : A user request object.

        - Returns:
          - TokenResponse : A TokenResponse objeto with user data and user access token.
        """

        model = await self.repository.get(email=request.email)

        if not model:

            raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        if not verify_password(request.password, model.password):

            raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        response = self.repository.map_model_to_response(model)

        return self.map_response_to_token(response)

    async def refresh_token(self, token: str) -> TokenResponse:
        """
        A method to refresh a user's token.

        - Args:
          - token: str : A user token.
        - Returns:
          - TokenResponse : A TokenResponse object with user data and user access token.
        """
        if not token:
            raise ValidationError(
                "token",
                ERROR_TOKEN_REQUIRED,
            )
        token_data = TokenData(**TokenManager.verify_token(token))

        model = await self.repository.get(id=token_data.user_id)

        if not model:

            raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        response = self.repository.map_model_to_response(model)

        return self.map_response_to_token(response)

    async def reset_password(self, email: str) -> str:
        """
        Reset a user's password.

        - Args:
            - email: str : A user email.

        - Returns:
            - str: new password generated
        """

        user = await self.repository.get(email=email)

        if user is None:
            raise NotFoundError(
                ERROR_DATABASE_USER_NOT_FOUND,
                local="services/user/reset_password",
            )

        new_password = generate_random_password()

        user.password = hash_password(new_password)

        await self.repository.update(user)

        return new_password

    @staticmethod
    def map_response_to_token(response: UserResponse) -> TokenResponse:
        """
        A method to map a user response to a token response.

        - Args:
            - response: UserResponse : A user response object.

        - Returns:
            - TokenResponse : A token response object.
        """

        return TokenResponse(
            access_token=TokenManager.create_access_token(
                data={
                    "user_id": response.id,
                    "user_role": response.role.value,
                }
            ),
            token_type="bearer",
            user=response,
        )
