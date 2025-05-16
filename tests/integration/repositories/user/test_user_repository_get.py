import pytest

from app.db.models import UserModel
from app.db.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_user_repository_get_by_id_success(
    mock_db_session, mock_user_model
):

    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    on_db = await repo.add(model)

    # Act

    response = await repo.get(id=on_db.id)

    # Assert

    assert on_db.name == response.name
    assert on_db.phone == response.phone
    assert on_db.email == response.email
    assert on_db.password == response.password
    assert on_db.role == response.role
    assert on_db.id == response.id
    assert on_db.created_at == response.created_at
    assert on_db.updated_at == response.updated_at


async def test_user_repository_get_by_email_success(
    mock_db_session, mock_user_model
):

    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    on_db = await repo.add(model)

    # Act

    response = await repo.get(email=on_db.email)

    # Assert

    assert on_db.name == response.name
    assert on_db.phone == response.phone
    assert on_db.email == response.email
    assert on_db.password == response.password
    assert on_db.role == response.role
    assert on_db.id == response.id
    assert on_db.created_at == response.created_at
    assert on_db.updated_at == response.updated_at


async def test_user_repository_get_all_success(
    mock_db_session, mock_user_model
):

    # Arrange

    data = mock_user_model.copy()

    model = UserModel(**data)

    db_session = mock_db_session

    repo = UserRepository(db_session)

    on_db = await repo.add(model)

    # Act

    responses = await repo.get(all_results=True)

    # Assert
    assert len(responses) == 1
    response = responses[0]
    assert on_db.name == response.name
    assert on_db.phone == response.phone
    assert on_db.email == response.email
    assert on_db.password == response.password
    assert on_db.role == response.role
    assert on_db.id == response.id
    assert on_db.created_at == response.created_at
    assert on_db.updated_at == response.updated_at


async def test_user_repository_get_none_success(
    mock_db_session, mock_user_model
):

    # Arrange

    db_session = mock_db_session

    repo = UserRepository(db_session)

    # Act

    responses = await repo.get()

    # Assert

    assert responses is None
