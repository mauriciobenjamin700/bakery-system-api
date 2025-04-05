import pytest

from app.core.constants.messages import ERROR_DATABASE_USER_NOT_FOUND, ERROR_REQUIRED_FIELD_ID
from app.core.errors import NotFoundError, ValidationError
from app.db.models import UserModel
from app.db.repositories.user import UserRepository

@pytest.mark.asyncio
async def test_user_repository_delete_by_id_success(mock_db_session, mock_user_model):

    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    on_db = await repo.add(model)

    # Act

    response = await repo.delete(id=on_db.id)


    # Assert

    assert response is None


async def test_user_repository_delete_by_model_success(mock_db_session, mock_user_model):
    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    on_db = await repo.add(model)

    # Act

    response = await repo.delete(model=on_db)

    # Assert

    assert response is None



async def test_user_repository_delete_fail_id_not_found(mock_db_session, mock_user_model):

    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    on_db = await repo.add(model)

    # Act

    with pytest.raises(NotFoundError) as e:
        await repo.delete(id="invalid_id")


    # Assert

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_USER_NOT_FOUND


async def test_user_repository_delete_fail_id_not_found(mock_db_session, mock_user_model):

    # Arrange

    db_session = mock_db_session

    repo = UserRepository(db_session)


    # Act

    with pytest.raises(ValidationError) as e:
        await repo.delete()

    # Assert

    assert e.value.status_code == 422
    assert e.value.field == "id"
    assert e.value.detail == ERROR_REQUIRED_FIELD_ID
