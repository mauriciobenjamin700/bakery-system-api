from pydantic import Field

from app.core.constants.enums.user import UserRoles
from app.schemas.settings.base import BaseSchema
from app.schemas.settings.validators import (
    validate_created_at,
    validate_email,
    validate_name,
    validate_password,
    validate_phone,
    validate_updated_at,
)


class UserBase(BaseSchema):
    """
    Class to contain data about the user.

    Attributes:
        id (str): The user's ID.
        name (str): The user's name.
        phone (str): The user's phone number.
        email (str): The user's email address.
    """

    name: str = Field(
        examples=["John Doe", "Jane Smith"],
        default=None,
        validate_default=True,
    )
    phone: str = Field(
        examples=["89912344321"], default=None, validate_default=True
    )
    email: str = Field(
        examples=["test@test.com"], default=None, validate_default=True
    )

    _name_validator = validate_name
    _phone_validator = validate_phone
    _email_validator = validate_email


class UserRequest(UserBase):
    """
    Class to validate the request body of the user register endpoint.

    Attributes:
        name (str): The user's name.
        phone (str): The user's phone number.
        email (str): The user's email address.
        password (str): The user's password.
    """

    password: str = Field(
        examples=["passWord123@"], default=None, validate_default=True
    )

    _password_validator = validate_password


class UserResponse(UserBase):
    """
    Class to contain data about the user.

    Attributes:
        id (str): The user's ID.
        name (str): The user's name.
        phone (str): The user's phone number.
        email (str): The user's email address.
        role (str): The user's role.
        created_at (str): The date and time when the user was created.
        updated_at (str): The date and time when the user was last updated.
    """

    id: str = Field(
        examples=["89912344321"], default=None, validate_default=True
    )
    role: UserRoles = Field(
        examples=[UserRoles.USER.value], default=None, validate_default=True
    )
    created_at: str = Field(
        examples=["2023-10-01 12:00:00"], default=None, validate_default=True
    )
    updated_at: str = Field(
        examples=["2023-10-01 12:00:00"], default=None, validate_default=True
    )
    _created_at_validator = validate_created_at
    _updated_at_validator = validate_updated_at


class LoginRequest(BaseSchema):
    """
    Class to validate the request body of the user login endpoint.

    Attributes:
        email (str): The user's email address.
        password (str): The user's password.
    """

    email: str = Field(
        examples=["test@gmai.com"], default=None, validate_default=True
    )
    password: str = Field(
        examples=["passWord123@"], default=None, validate_default=True
    )

    _email_validator = validate_email
    _password_validator = validate_password


class TokenData(BaseSchema):
    """
    Class to contain data about the user token.
    - Args:
        - user_id: str,
        - user_role: UserRoles
    - Attributes:
        - user_id: str,
        - user_role: UserRoles
    """

    user_id: str = Field(examples=["123456"])
    user_role: UserRoles = Field(examples=[UserRoles.USER])


class TokenResponse(BaseSchema):
    """
    Class to contain data about the user token response.
    - Args:
        - access_token: str,
        - user: UserResponse
    - Attributes:
        - access_token: str
        - token_type: str = "bearer"
        - user: UserResponse
    """

    access_token: str = Field(examples=["123456"])
    token_type: str = Field(examples=["bearer"], default="bearer")
    user: UserResponse
