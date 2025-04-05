import pytest

from app.core.constants.messages import *
from app.schemas.message import Message
from app.schemas.user import UserRequest
from app.services.user import UserService


@pytest.mark.asyncio
async def test_user_service_delete_success(mock_db_session, mock_user_request):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)
    on_db = await service.add(request)

    # Act

    response = await service.delete_by_id(on_db.id)

    # Assert
    isinstance(response, Message)
    assert response.detail == MESSAGE_USER_DELETE_SUCCESS
