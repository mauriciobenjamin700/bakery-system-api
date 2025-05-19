import pytest

from app.core.constants import messages
from app.core.errors import NotFoundError
from app.db.repositories import IngredientRepository
from app.schemas import IngredientRequest
from app.schemas.ingredient import IngredientBatchRequest


async def test_ingredient_repository_add_batch(
    mock_db_session, mock_ingredient_request, mock_ingredient_batch_request
) -> None:

    # Arrange

    repository = IngredientRepository(mock_db_session)
    ingredient_request = IngredientRequest(**mock_ingredient_request)
    ingredient_model = repository.map_request_to_model(
        ingredient_request, "image.jpg"
    )
    ingredient_model = await repository.add(ingredient_model)

    ingredient_batch_request = IngredientBatchRequest(
        **mock_ingredient_batch_request
    )
    ingredient_batch_request.ingredient_id = ingredient_model.id

    ingredient_batch_model = repository.map_batch_request_to_model(
        ingredient_batch_request
    )

    # Act

    ingredient_batch_model = await repository.add_batch(ingredient_batch_model)

    # Assert
    assert ingredient_batch_model.id is not None
    assert ingredient_batch_model.ingredient_id == ingredient_model.id
    assert ingredient_batch_model.created_at is not None
    assert ingredient_batch_model.updated_at is not None


async def test_ingredient_repository_add_batch_invalid_ingredient(
    mock_db_session, mock_ingredient_batch_request
) -> None:

    # Arrange

    repository = IngredientRepository(mock_db_session)

    ingredient_batch_request = IngredientBatchRequest(
        **mock_ingredient_batch_request
    )

    ingredient_batch_model = repository.map_batch_request_to_model(
        ingredient_batch_request
    )

    # Act
    with pytest.raises(NotFoundError) as e:
        await repository.add_batch(ingredient_batch_model)

    # Assert

    assert e.value.status_code == 404
    assert e.value.detail == messages.ERROR_DATABASE_INGREDIENT_NOT_FOUND
