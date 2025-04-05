from pydantic import Field
from app.core.constants.enums.user import UserRoles
from app.schemas.settings.base import BaseSchema
from app.schemas.settings.fields import(
    created_at_field,
    id_field,
    name_field,
    phone_field,
    email_field,
    password_field,
    updated_at_field,
)
from app.schemas.settings.validators import (
    validate_created_at,
    validate_email,
    validate_id,
    validate_name,
    validate_password,
    validate_phone,
    validate_updated_at,
)


class UserRequest(BaseSchema):
    """
    Class to validate the request body of the user register endpoint.

    - Args:
        - name: str,
        - phone: str,
        - email: str,
        - password: str

    - Attributes:
        - name: str,
        - phone: str,
        - email: str,
        - password: str

    - Raises:
        - ValidationError: If any field is invalid.
    """
    name: str = name_field()
    phone: str = phone_field()
    email: str = email_field()
    password: str = password_field()

    __name_validator = validate_name
    __phone_validator = validate_phone
    __email_validator = validate_email
    __password_validator = validate_password


class UserResponse(BaseSchema):
    """
    Class to contain data about the user.

    - Args:
        - id: str,
        - name: str,
        - phone: str,
        - email: str,
        - created_at: str,
        - updated_at: str

    - Attributes:
        - id: str,
        - name: str,
        - phone: str,
        - email: str,
        - created_at: str,
        - updated_at: str

    - Raises:
        - ValidationError: If any field is invalid
    """
    id: str = id_field()
    name: str = name_field()
    phone: str = phone_field()
    email: str = email_field()
    role: UserRoles = Field(examples=[UserRoles.USER.value])
    created_at: str = created_at_field()
    updated_at: str =  updated_at_field()

    __id_validator = validate_id
    __name_validator = validate_name
    __phone_validator = validate_phone
    __email_validator = validate_email
    __created_at_validator = validate_created_at
    __updated_at_validator = validate_updated_at
