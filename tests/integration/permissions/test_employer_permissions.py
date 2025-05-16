# from app.api.dependencies.permissions import employer_permission
# from app.schemas.user import TokenResponse


# async def test_employer_permissions(
#     mock_db_session,
#     mock_api
# ):

#     # Arrange

#     api = mock_api
#     session = mock_db_session


#     print(user_on_db)

#     token_response = await api.post(
#         "/user/login",
#         json=login
#     )

#     token_response = TokenResponse(**token_response.json())

#     token = token_response.access_token

#     # Act

#     response = await employer_permission(
#         token,
#         session
#     )

#     assert response.id == user_on_db.id
#     assert response.email == user_on_db.email
