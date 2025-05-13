from app.schemas.settings.base import BaseSchema


class ProductSold(BaseSchema):
    """
    Schema for the selling product.

    Attributes:
        id (str): The ID of the product.
        name (str): The name of the product.
        quantity (int): The quantity sold.
        total_price (float): The total price of the product sold.
    """

    id: str
    name: str
    quantity: int


class SellerResult(BaseSchema):
    """
    Schema for the seller result.

    Attributes:
        id (str): The ID of the seller.
        name (str): The name of the seller.
        total_sales (float): The total sales amount.
    """

    id: str
    name: str
    total_sales: float


class ProductReportResponse(BaseSchema):
    """
    Schema for the product report response.

    Attributes:
        top_selling_product (list[ProductSold]): List of top selling products.
        top_least_sold_products (list[ProductSold]): List of least sold products.
        sales_amount (float): Total sales amount.
        number_of_sales (int): Total number of sales.
        number_of_products (int): Total number of products.
        sales_profit (float): Total profit from sales.
        number_of_products_sold (int): Total number of products sold.
        mean_ticket (float): Average ticket value.
        top_seller (list[SellerResult]): List of top sellers.
    """

    top_selling_product: list[ProductSold]
    top_least_sold_products: list[ProductSold]
    sales_amount: float
    number_of_sales: int
    number_of_products: int
    sales_profit: float
    number_of_products_sold: int
    mean_ticket: float
    top_seller: list[SellerResult]
