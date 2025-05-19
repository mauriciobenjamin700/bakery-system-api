import pytest

from app.core.constants.messages import ERROR_DATABASE_USER_NOT_FOUND
from app.core.errors import NotFoundError
from app.core.security.password import verify_password
from app.schemas.user import UserRequest, UserResponse
from app.services.user import UserService


@pytest.mark.asyncio
async def test_user_service_update_success(mock_db_session, mock_user_request):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)
    response_db = await service.add(request)
    update = UserRequest(**request.to_dict())
    update.name = "New Name"
    update.email = "new@email.com"
    update.phone = "889123456789"
    update.password = "newPassword@"

    # Act

    response = await service.update(response_db.id, update)
    model = await service.repository.get(id=response_db.id)
    # Assert

    assert isinstance(response, UserResponse)
    assert response.name == update.name
    assert response.email == update.email
    assert response.phone == update.phone
    assert verify_password(update.password, model.password)


@pytest.mark.asyncio
async def test_user_service_update_fail_not_found(
    mock_db_session, mock_user_request
):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)

    await service.add(request)

    # Act

    with pytest.raises(NotFoundError) as e:
        await service.update("123", request)

    # Assert

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_USER_NOT_FOUND
