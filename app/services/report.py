# app/services/report.py

from datetime import datetime, timedelta
from typing import Sequence

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.db.models import ProductModel, SaleModel, UserModel
from app.db.repositories import ProductRepository, SaleRepository, UserRepository
from app.schemas.report import ProductReportResponse, ProductSold, SellerResult
from app.schemas.user import UserResponse 


class ReportService:
    def __init__(self, session: AsyncSession):
        self.product_repository = ProductRepository(session)
        self.sale_repository = SaleRepository(session)
        self.user_repository = UserRepository(session)

    async def get_product_report(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        top_n: int = 10,
    ) -> ProductReportResponse:
        response_data = {
            "top_selling_product": [],
            "top_least_sold_products": [],
            "sales_amount": 0.0,
            "number_of_sales": 0,
            "number_of_products": 0,
            "sales_profit": 0.0,
            "number_of_products_sold": 0,
            "mean_ticket": 0.0,
            "top_seller": []
        }

        products: Sequence[ProductModel] = await self.product_repository.get()  
        sales: Sequence[SaleModel] = await self.sale_repository.get(all_results=True) # type: ignore
        users: Sequence[UserModel] = await self.user_repository.get(all_results=True) # type: ignore

        if not products:
            return ProductReportResponse(**response_data)
        
        product_df = pd.DataFrame([product.to_dict() for product in products])

        if not sales:
            response_data["number_of_products"] = product_df["id"].nunique()
            return ProductReportResponse(**response_data)

        sale_df = pd.DataFrame([sale.to_dict() for sale in sales])

        # --- Debugging Step ---
        # Temporarily print columns and dtypes to verify 'quantity' and 'value'
        # print("Sale DataFrame columns:", sale_df.columns)
        # print("Sale DataFrame dtypes:\n", sale_df.dtypes)
        # --- End Debugging Step ---

        sale_df['created_at'] = pd.to_datetime(sale_df['created_at'])
        product_df['created_at'] = pd.to_datetime(product_df['created_at'])

        if start_date:
            sale_df = sale_df[(sale_df["created_at"] >= start_date)]
            product_df = product_df[(product_df["created_at"] >= start_date)]
        
        if end_date:
            sale_df = sale_df[(sale_df["created_at"] <= end_date)]
            product_df = product_df[(product_df["created_at"] <= end_date)]

        if sale_df.empty:
            response_data["number_of_products"] = product_df["id"].nunique()
            return ProductReportResponse(**response_data)
        if product_df.empty:
            return ProductReportResponse(**response_data)

        merged_df = sale_df.merge(
            product_df[["id", "name", "price_cost", "price_sale"]],
            left_on="product_id",
            right_on="id",
            how="left",
            suffixes=('_sale', '_product') # Adicionado suffixes novamente para garantir que 'quantity' de sale_df seja distinto
        )
        merged_df.rename(columns={'id_product': 'product_id_real'}, inplace=True) # Renomeia o id do produto mesclado
        quantity_col = 'quantity'
        if 'quantity_sale' in merged_df.columns:
            quantity_col = 'quantity_sale'
        elif 'quantity' not in merged_df.columns:
            # Isso seria um erro grave, significa que 'quantity' não veio do SaleModel.
            # Adicionar um log ou raise aqui para depuração se isso acontecer.
            raise ValueError("Coluna 'quantity' ou 'quantity_sale' não encontrada no merged_df. Verifique SaleModel e o merge.")

        merged_df['price_cost'] = merged_df['price_cost'].fillna(0)
        merged_df['price_sale'] = merged_df['price_sale'].fillna(0)
        merged_df['item_profit'] = (merged_df['price_sale'] - merged_df['price_cost']) * merged_df[quantity_col] # Usar a coluna correta


        response_data["sales_amount"] = float(merged_df["value"].sum())
        response_data["number_of_sales"] = int(sale_df["sale_code"].nunique())
        response_data["number_of_products"] = int(product_df["id"].nunique())
        response_data["sales_profit"] = float(merged_df['item_profit'].sum())
        response_data["number_of_products_sold"] = int(sale_df[quantity_col].sum()) # Usar a coluna correta

        response_data["mean_ticket"] = (
            (response_data["sales_amount"] / response_data["number_of_sales"])
            if response_data["number_of_sales"]
            else 0.0
        )

        # Top Selling Products (por quantidade)
        top_selling_product_df = (
            merged_df.groupby("product_id")
            .agg(
                quantity=pd.NamedAgg(column=quantity_col, aggfunc="sum"), # Usar a coluna correta
                total_price=pd.NamedAgg(column="value", aggfunc="sum"),
            )
            .reset_index()
            .sort_values(by="quantity", ascending=False)
        )
        top_selling_product_df = top_selling_product_df.merge(
            product_df[["id", "name"]],
            left_on="product_id",
            right_on="id",
            how="left",
        )
        response_data["top_selling_product"] = [
            ProductSold(id=str(row['id']), name=str(row['name']), quantity=int(row['quantity']), total_price=float(row['total_price']))
            for index, row in top_selling_product_df.head(top_n).iterrows()
        ]

        # Top Least Sold Products
        top_least_sold_products_df = top_selling_product_df.sort_values(by="quantity", ascending=True)
        response_data["top_least_sold_products"] = [
            ProductSold(id=str(row['id']), name=str(row['name']), quantity=int(row['quantity']), total_price=float(row['total_price']))
            for index, row in top_least_sold_products_df.head(top_n).iterrows()
        ]

        # Top Seller (needs user names from UserModel)
        if users:
            user_df = pd.DataFrame([user.to_dict() for user in users])
            
            top_seller_df = (
                sale_df.groupby("user_id").agg({"value": "sum"}).reset_index()
            )
            top_seller_df = top_seller_df.merge(
                user_df[["id", "name"]],
                left_on="user_id",
                right_on="id",
                how="left",
            )
            top_seller_df = top_seller_df.sort_values(by="value", ascending=False).head(top_n)
            top_seller_df.rename(columns={"value": "total_sales"}, inplace=True)
            response_data["top_seller"] = [
                SellerResult(id=str(row['user_id']), name=str(row['name']), total_sales=float(row['total_sales']))
                for index, row in top_seller_df.iterrows()
            ]

        return ProductReportResponse(**response_data)