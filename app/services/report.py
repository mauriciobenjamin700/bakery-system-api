from datetime import datetime
from typing import Sequence

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.db.models import ProductModel, SaleModel
from app.db.repositories import ProductRepository, SaleRepository
from app.schemas import ProductReportResponse


class ReportService:
    """
    Service class for handling report operations.

    Methods:
        - get_product_report: Generates a report of all products.
    """

    def __init__(self, session: AsyncSession):
        self.product_repository = ProductRepository(session)
        self.sale_repository = SaleRepository(session)

    async def get_product_report(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        top_n: int = 10,
    ) -> ProductReportResponse:
        """
        # A method to generate a report of all products.

        ## Returns:
            - dict: A dictionary containing the product report.
        """

        response = {}

        products: Sequence[ProductModel] = await self.product_repository.get()  # type: ignore

        if products is None:
            raise NotFoundError("No products found")

        sales: list[SaleModel] = await self.sale_repository.get(
            all_results=True  # type: ignore
        )

        if not sales:
            raise NotFoundError("No sales found")

        product_df = pd.DataFrame(
            [product.to_dict() for product in products],
            columns=[
                "id",
                "name",
                "price_cost",
                "price_sale",
                "measure",
                "mark",
                "created_at",
                "updated_at",
            ],
        )

        sale_df = pd.DataFrame(
            [sale.to_dict() for sale in sales],
            columns=[
                "id",
                "product_id",
                "user_id",
                "is_paid" "quantity",
                "value",
                "sale_code",
                "created_at",
            ],
        )

        if start_date and end_date:
            sale_df = sale_df[
                (sale_df["created_at"] >= start_date)
                & (sale_df["created_at"] <= end_date)
            ]
            product_df = product_df[
                (product_df["created_at"] >= start_date)
                & (product_df["created_at"] <= end_date)
            ]
        elif start_date:
            sale_df = sale_df[sale_df["created_at"] == start_date]
            product_df = product_df[product_df["created_at"] == start_date]

        elif end_date:
            sale_df = sale_df[sale_df["created_at"] == end_date]
            product_df = product_df[product_df["created_at"] == end_date]

        if sale_df.empty:
            raise NotFoundError("No sales found in the specified date range")
        if product_df.empty:
            raise NotFoundError(
                "No products found in the specified date range"
            )

        top_selling_product = (
            sale_df.groupby("product_id")
            .agg({"quantity": "sum"})
            .reset_index()
            .sort_values(by="quantity", ascending=False)
        )

        top_selling_product = top_selling_product.merge(
            product_df[["id", "name"]],
            left_on="product_id",
            right_on="id",
            how="left",
        )

        top_selling_product = top_selling_product[
            ["id", "name", "quantity"]
        ].head(top_n)
        response["top_selling_product"] = top_selling_product.to_dict(
            orient="records"
        )

        top_least_sold_products = top_selling_product[
            ["id", "name", "quantity"]
        ].head(-top_n)
        response["top_least_sold_products"] = top_least_sold_products.to_dict(
            orient="records"
        )

        sales_amount: float = sale_df["value"].sum()
        response["sales_amount"] = sales_amount

        number_of_sales: int = sale_df["id"].nunique()
        response["number_of_sales"] = number_of_sales

        number_of_products: int = product_df["id"].nunique()
        response["number_of_products"] = number_of_products

        sales_profit = (
            product_df["price_sale"].sum() - product_df["price_cost"].sum()
        )
        response["sales_profit"] = sales_profit

        number_of_products_sold: int = sale_df["quantity"].sum()
        response["number_of_products_sold"] = number_of_products_sold

        mean_ticket = (
            (sales_amount / number_of_products_sold)
            if number_of_products_sold
            else 0
        )
        response["mean_ticket"] = mean_ticket

        top_seller = (
            sale_df.groupby("user_id").agg({"value": "sum"}).reset_index()
        )
        top_seller = top_seller.merge(
            product_df[["id", "name"]],
            left_on="user_id",
            right_on="id",
            how="left",
        )
        top_seller = top_seller[["id", "name", "value"]].head(top_n)
        top_seller.rename(columns={"value": "total_sales"}, inplace=True)
        response["top_seller"] = top_seller.to_dict(orient="records")

        return ProductReportResponse(**response)
