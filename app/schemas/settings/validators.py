from datetime import datetime

from pydantic import field_validator

from app.core.constants.messages import *
from app.core.errors import ValidationError
from app.utils.validators import (
    parse_date_to_string,
    parse_email,
    parse_phone,
    parse_string,
)


@field_validator("created_at", mode="before")
def validate_created_at(cls, value: datetime | str) -> str | None:
    """
    A function that validates the created_at field.

    Args:
        cls: The class instance.
        value: The created_at value.
    Returns:
        str: The created_at value.
    """

    return parse_date_to_string(value)


@field_validator("description", mode="before")
def validate_description(cls, value: str) -> str | None:
    """
    A function that validates the description field.

    - Args:
        - cls: The class instance.
        - value: The description value.
    - Returns:
        - str: The description value.
    """
    return parse_string(value)


@field_validator("email", mode="before")
def validate_email(cls, value: str) -> str:
    """
    A function that validates the email field.

    - Args:
        - cls: The class instance.
        - value: The email value.
    - Returns:
        - str: The email value.
    """
    value = parse_string(value)

    if not isinstance(value, str):
        raise ValidationError(
            field="email", detail=ERROR_INVALID_FORMAT_TYPE_EMAIL
        )

    value = parse_email(value)

    if not value:
        raise ValidationError(
            field="email", detail=ERROR_EMAIL_INVALID_FORMAT_MASK
        )

    return value


@field_validator("mark", mode="before")
def validate_mark(cls, value: str) -> str | None:
    """
    A function that validates the mark field.

    - Args:
        - cls: The class instance.
        - value: The mark value.
    - Returns:
        - str: The mark value.
    """
    return parse_string(value)


@field_validator("name", mode="before")
def validate_name(cls, value: str) -> str:
    """
    A function that validates the name field.

    - Args:
        - cls: The class instance.
        - value: The name value.
    - Returns:
        - str: The name value.
    """
    value = parse_string(value)

    if value:
        if len(value) <= 1:
            raise ValidationError(
                field="name", detail=ERROR_NAME_INVALID_FORMAT_MIN_LENGTH
            )

    return value


@field_validator("password", mode="before")
def validate_password(cls, value: str) -> str:
    """
    A function that validates the password field.

    - Args:
        - cls: The class instance.
        - value: The password value.
    - Returns:
        - str: The password value.
    """

    value = parse_string(value)

    if value:

        if len(value) < 8:
            raise ValidationError(
                field="password",
                detail=ERROR_PASSWORD_INVALID_FORMAT_MIN_LENGTH,
            )

        if len(value) > 255:
            raise ValidationError(
                field="password",
                detail=ERROR_PASSWORD_INVALID_FORMAT_MAX_LENGTH,
            )

        if not any(char.isdigit() for char in value):
            raise ValidationError(
                field="password", detail=ERROR_PASSWORD_INVALID_FORMAT_DIGIT
            )

        if not any(char.islower() for char in value):
            raise ValidationError(
                field="password",
                detail=ERROR_PASSWORD_INVALID_FORMAT_LOWERCASE,
            )

        if not any(char.isupper() for char in value):
            raise ValidationError(
                field="password",
                detail=ERROR_PASSWORD_INVALID_FORMAT_UPPERCASE,
            )

        if not any(char in "!@#$%&*()_+-=[]{};:,.<>?/" for char in value):
            raise ValidationError(
                field="password",
                detail=ERROR_PASSWORD_INVALID_FORMAT_SPECIAL_CHARACTER,
            )

    return value


@field_validator("phone", mode="before")
def validate_phone(cls, value: str) -> str | None:
    """
    A function that validates the phone field.

    - Args:
        - cls: The class instance.
        - value: The phone value.
    - Returns:
        - str: The phone value.
    """
    value = parse_string(value)
    if value:
        value = parse_phone(value)

        if not value:
            raise ValidationError(
                field="phone", detail=ERROR_PHONE_INVALID_FORMAT_TYPE
            )

        if len(value) < 11:
            raise ValidationError(
                field="phone", detail=ERROR_PHONE_INVALID_FORMAT_LENGTH
            )

    return value


@field_validator("updated_at", mode="before")
def validate_updated_at(cls, value: datetime | str) -> str:
    """
    Validates the updated_at field.

    Args
        cls: The class instance.
        value: The value to validate.
    Returns
        str: The validated value.
    """
    value = parse_date_to_string(value)

    if not value:

        raise ValidationError(
            field="updated_at", detail=ERROR_DATE_INVALID_FORMAT_MASK
        )

    return value
