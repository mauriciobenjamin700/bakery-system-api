import pytest

from app.schemas import ProductRequest, SaleRequest, UserRequest
from app.schemas.sale import SaleResponse
from app.services import ProductService, SaleService, UserService


async def test_sale_service_add_success(
    mock_db_session,
    mock_product_request_with_no_recipe,
    mock_user_request,
    mock_sale_request,
):
    user_service = UserService(mock_db_session)

    user_request = UserRequest(**mock_user_request)

    user_response = await user_service.add(user_request)

    product_service = ProductService(mock_db_session)

    product_request = ProductRequest(**mock_product_request_with_no_recipe)

    product_response = await product_service.add(
        product_request, "product.jpg"
    )

    sale_service = SaleService(mock_db_session)

    sale_request = SaleRequest(
        product_id=product_response.id,
        user_id=user_response.id,
        quantity=mock_sale_request["quantity"],
    )

    response = await sale_service.add(sale_request)

    assert isinstance(response, SaleResponse)
    assert response.product_id == product_response.id
    assert response.user_id == user_response.id
    assert response.quantity == sale_request.quantity
    assert response.is_paid is False
    assert (
        response.value == product_response.price_sale * sale_request.quantity
    )
    assert isinstance(response.sale_code, str)
    assert isinstance(response.created_at, str)
