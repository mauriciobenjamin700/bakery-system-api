from pydantic import ValidationError as PydanticValidationError
from pytest import raises

from app.core.constants.messages import *
from app.core.errors import ValidationError
from app.schemas.user import UserRequest
from app.utils.validators import parse_phone


def test_user_request_validation_success(mock_user_request):

    # Arrange

    data = mock_user_request.copy()

    # Act

    request = UserRequest(**data)

    # Assert

    assert request.name == (data.get("name"))
    assert request.phone == parse_phone(data.get("phone"))
    assert request.email == data.get("email")
    assert request.password == data.get("password")


def test_user_request_validation_error_not_name(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    del data["name"]

    # Act

    with raises(PydanticValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.errors()[0]["loc"] == ("name",)


def test_user_request_validation_error_just_spaces_name(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    data["name"] = "   "

    # Act

    with raises(PydanticValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.errors()[0]["loc"] == ("name",)


def test_user_request_validation_error_not_phone(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    del data["phone"]

    # Act

    with raises(PydanticValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.errors()[0]["loc"] == ("phone",)


def test_user_request_validation_error_just_spaces_phone(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    data["phone"] = "   "

    # Act

    with raises(PydanticValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.errors()[0]["loc"] == ("phone",)


def test_user_request_validation_error_not_email(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    del data["email"]

    # Act

    with raises(ValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.field == "email"
    assert error.value.detail == ERROR_INVALID_FORMAT_TYPE_EMAIL


def test_user_request_validation_error_invalid_email(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    data["email"] = "invalid_email"

    # Act

    with raises(ValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.field == "email"
    assert error.value.detail == ERROR_EMAIL_INVALID_FORMAT_MASK


def test_user_request_validation_error_not_password(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    del data["password"]

    # Act

    with raises(PydanticValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.errors()[0]["loc"] == ("password",)


def test_user_request_validation_error_just_spaces_password(mock_user_request):

    # Arrange

    data = mock_user_request.copy()
    data["password"] = "   "

    # Act

    with raises(PydanticValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.errors()[0]["loc"] == ("password",)


def test_user_request_validation_error_invalid_password_max_length(
    mock_user_request,
):

    # Arrange

    data = mock_user_request.copy()
    data["password"] = "a" * 256

    # Act

    with raises(ValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.field == "password"
    assert error.value.detail == ERROR_PASSWORD_INVALID_FORMAT_MAX_LENGTH


def test_user_request_validation_error_invalid_password_no_digit(
    mock_user_request,
):

    # Arrange

    data = mock_user_request.copy()
    data["password"] = "invalid_password"

    # Act

    with raises(ValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.field == "password"
    assert error.value.detail == ERROR_PASSWORD_INVALID_FORMAT_DIGIT


def test_user_request_validation_error_invalid_password_no_lower_case(
    mock_user_request,
):

    # Arrange

    data = mock_user_request.copy()
    data["password"] = "INVALID_PASSWORD1"

    # Act

    with raises(ValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.field == "password"
    assert error.value.detail == ERROR_PASSWORD_INVALID_FORMAT_LOWERCASE


def test_user_request_validation_error_invalid_password_no_upper_case(
    mock_user_request,
):

    # Arrange

    data = mock_user_request.copy()
    data["password"] = "invalid_password1"

    # Act

    with raises(ValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.field == "password"
    assert error.value.detail == ERROR_PASSWORD_INVALID_FORMAT_UPPERCASE


def test_user_request_validation_error_invalid_password_no_special_character(
    mock_user_request,
):

    # Arrange

    data = mock_user_request.copy()
    data["password"] = "invalidpassword1A"

    # Act

    with raises(ValidationError) as error:
        UserRequest(**data)
    # Assert

    assert error.value.field == "password"
    assert (
        error.value.detail == ERROR_PASSWORD_INVALID_FORMAT_SPECIAL_CHARACTER
    )
