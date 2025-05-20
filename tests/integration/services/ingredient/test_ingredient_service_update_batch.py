import pytest

from app.core.constants.messages import (
    ERROR_DATABASE_INGREDIENT_BATCH_NOT_FOUND,
)
from app.core.errors import NotFoundError
from app.schemas import (
    IngredientBatchRequest,
    IngredientBatchUpdate,
    IngredientRequest,
)
from app.schemas.ingredient import IngredientBatchResponse
from app.services import IngredientService


async def test_ingredient_service_update_batch_success(
    mock_db_session,
    mock_ingredient_request,
    mock_ingredient_batch_request,
    mock_ingredient_batch_update,
):

    request = IngredientRequest(**mock_ingredient_request)
    service = IngredientService(mock_db_session)

    ingredient = await service.add(request, "test.png")

    batch_request = IngredientBatchRequest(**mock_ingredient_batch_request)

    batch_request.ingredient_id = ingredient.id

    response = await service.add_batch(batch_request)

    update = IngredientBatchUpdate(**mock_ingredient_batch_update)

    updated = await service.update_batch(
        response.id,
        update,
    )

    ingredient = await service.get_by_id(ingredient.id)

    assert isinstance(updated, IngredientBatchResponse)
    assert updated.created_at is not None
    assert updated.updated_at is not None
    assert updated.ingredient_id == ingredient.id
    assert updated.quantity != response.quantity
    assert len(ingredient.batches) == 2


async def test_ingredient_service_update_batch_not_found(
    mock_db_session, mock_ingredient_batch_update
):

    service = IngredientService(mock_db_session)

    update = IngredientBatchUpdate(**mock_ingredient_batch_update)

    with pytest.raises(NotFoundError) as e:
        await service.update_batch(
            "1",
            update,
        )

    assert e.value.detail == ERROR_DATABASE_INGREDIENT_BATCH_NOT_FOUND
    assert e.value.status_code == 404
