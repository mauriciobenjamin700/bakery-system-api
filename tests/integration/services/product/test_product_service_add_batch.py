from app.schemas import ProductRequest, ProductResponse, ProductBatchRequest
from app.services import IngredientService, ProductService


async def test_product_service_add_batch_success(
    mock_db_session, 
    mock_product_request_with_no_recipe,
    mock_product_batch_request

):
    request = ProductRequest(**mock_product_request_with_no_recipe)
    service = ProductService(mock_db_session)

    product = await service.add(request, "test.png")

    batch_request = ProductBatchRequest(**mock_product_batch_request)

    batch_request.product_id = product.id

    response = await service.add_product_batch(batch_request)

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
    assert response.quantity == request.quantity + batch_request.quantity
    assert response.recipe is None
    assert isinstance(response.batches, list)
    assert len(response.batches) == 2
    assert response.created_at is not None
    assert response.updated_at is not None