import pytest
from app.core.constants.messages import ERROR_DATABASE_USER_NOT_FOUND
from app.core.errors import NotFoundError
from app.schemas.user import LoginRequest, TokenResponse
from app.services.user import UserService
from tests.utils import (
    mock_user_employer_on_db,
    mock_user_employer_login
)


async def test_user_service_login_success(
    mock_db_session
):
    
    # Arrange
    session = mock_db_session
    service = UserService(mock_db_session)
    user = await mock_user_employer_on_db(session)
    login = LoginRequest(**mock_user_employer_login())
    
    print(user)
    
    print(login)

    # Act

    response = await service.login(login)

    # Assert

    assert response
    assert isinstance(response, TokenResponse)
    assert response.user.id == user.id
    
    
async def test_user_service_login_fail_by_email(
    mock_db_session
):
    
    # Arrange
    
    login = LoginRequest(
        email="test@fail.com",
        password="12345678Ab-"
    )
    
    service = UserService(mock_db_session)
    
    # Act
    
    with pytest.raises(NotFoundError) as e:
        
        await service.login(login)
        
    # Assert
    
    e.value.status_code == 404
    e.value.detail == ERROR_DATABASE_USER_NOT_FOUND
    
    
async def test_user_service_login_fail_by_password(
    mock_db_session
):
    
    # Arrange
    
    session = mock_db_session
    service = UserService(mock_db_session)
    user = await mock_user_employer_on_db(session)
    
    login = LoginRequest(
        email=user.email,
        password="12345678Ab-"
    )
    
    # Act
    
    with pytest.raises(NotFoundError) as e:
        
        await service.login(login)
        
    # Assert
    
    e.value.status_code == 404
    e.value.detail == ERROR_DATABASE_USER_NOT_FOUND