from app.db.models import UserModel


def test_user_model(mock_user_model):

    # Arrange

    data = mock_user_model

    # Act

    user = UserModel(**data)

    # Assert
    assert user.name == data.get("name")
    assert user.phone == data.get("phone")
    assert user.email == data.get("email")
    assert user.password == data.get("password")
    assert user.role == data.get("role")
    assert user.created_at is None
    assert user.updated_at is None
    assert user.id is None
