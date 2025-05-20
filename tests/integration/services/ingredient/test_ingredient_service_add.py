from app.schemas import IngredientRequest, IngredientResponse
from app.services import IngredientService


async def test_ingredient_service_add_success(
    mock_db_session, mock_ingredient_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    response = await service.add(request, "test.png")

    assert isinstance(response, IngredientResponse)
    assert response.created_at is not None
    assert response.updated_at is not None
    assert response.batches is not None
    assert len(response.batches) == 1
