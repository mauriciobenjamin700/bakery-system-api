from datetime import datetime

import pytest

from app.core.constants import messages
from app.core.errors import ConflictError
from app.db.models import IngredientModel
from app.db.repositories.ingredient import IngredientRepository


async def test_ingredient_repository_add(
    mock_db_session, mock_ingredient_model
) -> None:

    # Arrange

    repository = IngredientRepository(mock_db_session)
    model = IngredientModel(**mock_ingredient_model)

    # Act

    response = await repository.add(model)

    assert isinstance(response, IngredientModel)
    assert response.id
    assert response.name == mock_ingredient_model["name"]
    assert response.measure == mock_ingredient_model["measure"]
    assert response.image_path == mock_ingredient_model["image_path"]
    assert response.mark == mock_ingredient_model["mark"]
    assert response.description == mock_ingredient_model["description"]
    assert response.value == mock_ingredient_model["value"]
    assert response.min_quantity == mock_ingredient_model["min_quantity"]
    assert isinstance(response.created_at, datetime)
    assert isinstance(response.updated_at, datetime)


async def test_ingredient_repository_add_already_exists(
    mock_db_session, mock_ingredient_model
):

    # Arrange

    repository = IngredientRepository(mock_db_session)
    model = IngredientModel(**mock_ingredient_model)
    await repository.add(model)

    # Act

    with pytest.raises(ConflictError) as e:
        await repository.add(model)

    assert e.value.detail == messages.ERROR_DATABASE_INGREDIENT_ALREADY_EXISTS
    assert e.value.status_code == 409
