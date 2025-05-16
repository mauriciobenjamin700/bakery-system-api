import pytest

from app.db.models import UserModel
from app.db.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_user_repository_add_success(mock_db_session, mock_user_model):

    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    # Act

    on_db = await repo.add(model)

    # Assert

    assert on_db.name == model.name
    assert on_db.phone == model.phone
    assert on_db.email == model.email
    assert on_db.password == model.password
    assert on_db.role == model.role
    assert on_db.id is not None
    assert on_db.created_at is not None
    assert on_db.updated_at is not None
