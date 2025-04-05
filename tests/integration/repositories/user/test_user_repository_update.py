import pytest
from time import sleep

from app.db.models import UserModel
from app.db.repositories.user import UserRepository

@pytest.mark.asyncio
async def test_user_repository_update_success(mock_db_session, mock_user_model):

    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    on_db = await repo.add(model)

    update = {
        "name": "Updated Name",
        "phone": "89912347788",
        "email": "new@email.com",
        "password": model.password,
        "role": model.role,
        "id": model.id,
        "created_at": model.created_at,
        "updated_at": model.updated_at
    }

    on_db.name = update.get("name")
    on_db.phone = update.get("phone")
    on_db.email = update.get("email")

    # Act

    sleep(1)

    response = await repo.update(on_db)


    # Assert

    assert update.get("name") == response.name
    assert update.get("phone") == response.phone
    assert update.get("email") == response.email
    assert update.get("password") == response.password
    assert update.get("role") == response.role
    assert update.get("id") == response.id
    assert update.get("created_at") == response.created_at
    assert update.get("updated_at") != response.updated_at
