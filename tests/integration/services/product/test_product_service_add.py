from app.schemas import ProductRequest, ProductResponse
from app.services import ProductService


async def test_product_service_add_success(
    mock_db_session, mock_product_request_with_no_recipe
):
    request = ProductRequest(**mock_product_request_with_no_recipe)
    service = ProductService(mock_db_session)

    response = await service.add(request, "test.png")

    assert isinstance(response, ProductResponse)
    assert response.name == request.name
    assert response.description == request.description
    assert response.image_path == "test.png"
