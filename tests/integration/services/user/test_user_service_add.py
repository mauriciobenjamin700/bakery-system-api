import pytest

from app.core.constants.messages import ERROR_DATABASE_USER_ALREADY_EXISTS
from app.core.errors import ConflictError
from app.schemas.user import UserRequest, UserResponse
from app.services.user import UserService


@pytest.mark.asyncio
async def test_user_service_add_success(mock_db_session, mock_user_request):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)

    # Act

    response = await service.add(request)

    # Assert

    assert isinstance(response, UserResponse)
    assert response.id
    assert isinstance(response.id, str)
    assert response.name == request.name
    assert response.email == request.email
    assert response.phone == request.phone
    assert response.created_at
    assert response.updated_at
    assert isinstance(response.created_at, str)
    assert isinstance(response.updated_at, str)


@pytest.mark.asyncio
async def test_user_service_add_fail_already_exists(
    mock_db_session, mock_user_request
):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)

    await service.add(request)

    # Act

    with pytest.raises(ConflictError) as e:
        await service.add(request)

    # Assert

    assert e.value.status_code == 409
    assert e.value.detail == ERROR_DATABASE_USER_ALREADY_EXISTS
