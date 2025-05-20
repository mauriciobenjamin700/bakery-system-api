from app.schemas import IngredientBatchRequest, IngredientRequest
from app.schemas.ingredient import IngredientBatchResponse
from app.services import IngredientService


async def test_ingredient_service_add_batch_success(
    mock_db_session, mock_ingredient_request, mock_ingredient_batch_request
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    ingredient = await service.add(request, "test.png")

    batch_request = IngredientBatchRequest(**mock_ingredient_batch_request)

    batch_request.ingredient_id = ingredient.id

    response = await service.add_batch(batch_request)

    ingredient = await service.get_by_id(ingredient.id)

    assert isinstance(response, IngredientBatchResponse)
    assert response.created_at is not None
    assert response.updated_at is not None
    assert response.ingredient_id == ingredient.id
    assert response.quantity == batch_request.quantity
    assert len(ingredient.batches) == 2
