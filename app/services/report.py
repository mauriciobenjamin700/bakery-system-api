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

        products: Sequence[ProductModel] = await self.product_repository.get()  

        if not products:
            raise NotFoundError("No products found")

        sales: list[SaleModel] = await self.sale_repository.get(
            all_results=True  
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
                "is_paid", "quantity",
                "value",
                "sale_code",
                "created_at",
            ],
        )

        
        sale_df["created_at"] = pd.to_datetime(sale_df["created_at"])
        product_df["created_at"] = pd.to_datetime(product_df["created_at"])


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
           
            end_of_day = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59, 999999)
            sale_df = sale_df[
                (sale_df["created_at"] >= start_date)
                & (sale_df["created_at"] <= end_of_day)
            ]
            product_df = product_df[
                (product_df["created_at"] >= start_date)
                & (product_df["created_at"] <= end_of_day)
            ]
        elif end_date:
           
            end_of_day = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, 999999)
            sale_df = sale_df[
                (sale_df["created_at"] >= end_date.replace(hour=0, minute=0, second=0, microsecond=0))
                & (sale_df["created_at"] <= end_of_day)
            ]
            product_df = product_df[
                (product_df["created_at"] >= end_date.replace(hour=0, minute=0, second=0, microsecond=0))
                & (product_df["created_at"] <= end_of_day)
            ]

       
        if sale_df.empty:
            raise NotFoundError("No sales found in the specified date range")
        if product_df.empty:
            
            raise NotFoundError("No products found in the specified date range")


        # --- TOP SELLING PRODUCTS ---
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
        
        top_selling_product['name'] = top_selling_product['name'].fillna('Produto Desconhecido')
        top_selling_product['id'] = top_selling_product['id'].fillna('') 
        top_selling_product['quantity'] = top_selling_product['quantity'].fillna(0) 

        top_selling_product = top_selling_product[
            ["id", "name", "quantity"]
        ].head(top_n)
        response["top_selling_product"] = top_selling_product.to_dict(
            orient="records"
        )

       
        top_least_sold_products = (
            sale_df.groupby("product_id")
            .agg({"quantity": "sum"})
            .reset_index()
            .sort_values(by="quantity", ascending=True) 
        )

        top_least_sold_products = top_least_sold_products.merge(
            product_df[["id", "name"]],
            left_on="product_id",
            right_on="id",
            how="left",
        )
        
        top_least_sold_products['name'] = top_least_sold_products['name'].fillna('Produto Desconhecido')
        top_least_sold_products['id'] = top_least_sold_products['id'].fillna('')
        top_least_sold_products['quantity'] = top_least_sold_products['quantity'].fillna(0)

        top_least_sold_products = top_least_sold_products[
            ["id", "name", "quantity"]
        ].head(top_n) 
        response["top_least_sold_products"] = top_least_sold_products.to_dict(
            orient="records"
        )

        
        sales_amount: float = sale_df["value"].sum()
        response["sales_amount"] = sales_amount if not pd.isna(sales_amount) else 0.0 # Tratando NaN de soma de vazios


        
        number_of_sales: int = sale_df["id"].nunique()
        response["number_of_sales"] = number_of_sales


       
        number_of_products: int = product_df["id"].nunique()
        response["number_of_products"] = number_of_products


       
        total_price_sale = product_df["price_sale"].sum() if not product_df.empty else 0.0
        total_price_cost = product_df["price_cost"].sum() if not product_df.empty else 0.0
        sales_profit = total_price_sale - total_price_cost
        response["sales_profit"] = sales_profit if not pd.isna(sales_profit) else 0.0 # Tratando NaN


        
        number_of_products_sold: float = sale_df["quantity"].sum() 
        response["number_of_products_sold"] = int(number_of_products_sold) if not pd.isna(number_of_products_sold) else 0 

        
        mean_ticket = (
            (sales_amount / number_of_products_sold)
            if number_of_products_sold > 0 
            else 0.0 
        )
        response["mean_ticket"] = mean_ticket


       
        top_seller = (
            sale_df.groupby("user_id").agg({"value": "sum"}).reset_index()
        )
        top_seller['value'] = top_seller['value'].fillna(0) 
        top_seller['user_id'] = top_seller['user_id'].astype(str) 

        top_seller = top_seller[["user_id", "value"]].head(top_n)
        top_seller.rename(columns={"value": "total_sales", "user_id": "id"}, inplace=True)

        final_top_seller_list = []
        for index, row in top_seller.iterrows():
            final_top_seller_list.append({
                "id": str(row["id"]), 
                
                "name": f"Usuário {row['id']}",
                "total_sales": float(row["total_sales"]) 
            })
        response["top_seller"] = final_top_seller_list

       
        print(f"DEBUG FINAL RESPONSE: {response}")


        return ProductReportResponse(**response)