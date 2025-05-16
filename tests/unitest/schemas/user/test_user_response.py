from app.schemas import UserResponse


def test_user_response_success(mock_user_response):

    data = mock_user_response.copy()

    schema = UserResponse(**data)

    assert schema.id == data["id"]
    assert schema.name == data["name"]
    assert schema.phone == data["phone"]
    assert schema.email == data["email"]
    assert schema.role.value == data["role"]
    assert isinstance(schema.created_at, str)
    assert isinstance(schema.updated_at, str)
