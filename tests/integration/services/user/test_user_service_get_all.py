import pytest

from app.core.constants.messages import ERROR_DATABASE_USERS_NOT_FOUND
from app.core.errors import NotFoundError
from app.schemas.user import UserRequest, UserResponse
from app.services.user import UserService


@pytest.mark.asyncio
async def test_user_service_get_all_success(
    mock_db_session, mock_user_request
):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)
    response_db = await service.add(request)

    # Act

    response = await service.get_all()

    # Assert
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], UserResponse)
    assert response[0] == response_db


@pytest.mark.asyncio
async def test_user_service_get_fail_not_found(mock_db_session):

    # Arrange

    service = UserService(mock_db_session)
    # Act

    with pytest.raises(NotFoundError) as e:
        await service.get_all()

    # Assert

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_USERS_NOT_FOUND
