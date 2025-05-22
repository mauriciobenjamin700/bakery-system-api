from app.schemas import ProductRequest, ProductResponse
from app.schemas.ingredient import IngredientRequest
from app.services import IngredientService, ProductService


async def test_product_service_add_success_with_no_recipe(
    mock_db_session, mock_product_request_with_no_recipe
):
    request = ProductRequest(**mock_product_request_with_no_recipe)
    service = ProductService(mock_db_session)

    response = await service.add(request, "test.png")

    assert isinstance(response, ProductResponse)
    assert response.name == request.name
    assert response.price_cost == request.price_cost
    assert response.price_sale == request.price_sale
    assert response.measure.value == request.measure.value
    assert response.description == request.description
    assert response.mark == request.mark
    assert response.min_quantity == request.min_quantity
    assert response.id is not None
    assert response.image_path == "test.png"
    assert response.quantity == request.quantity
    assert response.recipe is None
    assert isinstance(response.batches, list)
    assert len(response.batches) == 1
    assert response.batches[0].quantity == request.quantity
    assert response.created_at is not None
    assert response.updated_at is not None

async def test_product_service_add_success_with_recipe(
    mock_db_session, 
    mock_product_request_with_recipe,
    mock_list_ingredient_request
):
    request = ProductRequest(**mock_product_request_with_recipe)
    service = ProductService(mock_db_session)
    ingredients = [
        IngredientRequest(**data)
        for data in mock_list_ingredient_request
    ]

    ingredients_on_db = []

    ingredient_service = IngredientService(mock_db_session)

    for ingredient in ingredients:
        ingredient_response = await ingredient_service.add(ingredient, "default.png")
        ingredients_on_db.append(ingredient_response)

    for idx in range(len(request.recipe)):
        request.recipe[idx].ingredient_id = ingredients_on_db[idx].id

    response = await service.add(request, "test.png")

    assert isinstance(response, ProductResponse)
    assert response.name == request.name
    assert response.price_cost == request.price_cost
    assert response.price_sale == request.price_sale
    assert response.measure.value == request.measure.value
    assert response.description == request.description
    assert response.mark == request.mark
    assert response.min_quantity == request.min_quantity
    assert response.id is not None
    assert response.image_path == "test.png"
    assert response.quantity == request.quantity
    assert isinstance(response.recipe, list)
    assert len(response.recipe) == len(request.recipe)
    assert isinstance(response.batches, list)
    assert len(response.batches) == 1
    assert response.batches[0].quantity == request.quantity
    assert response.created_at is not None
    assert response.updated_at is not None