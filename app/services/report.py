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
                "is_paid", "quantity", # <-- VÍRGULA CORRIGIDA AQUI
                "value",
                "sale_code",
                "created_at",
            ],
        )

        # Converte a coluna 'created_at' para datetime para permitir filtragem
        sale_df["created_at"] = pd.to_datetime(sale_df["created_at"])
        product_df["created_at"] = pd.to_datetime(product_df["created_at"])

        # Lógica de filtragem por data
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
            # Filtra do start_date até o final do dia do start_date
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
            # Filtra do início do dia do end_date até o final do dia do end_date
            start_of_day = datetime(end_date.year, end_date.month, end_date.day, 0, 0, 0, 0)
            end_of_day = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, 999999)
            sale_df = sale_df[
                (sale_df["created_at"] >= start_of_day)
                & (sale_df["created_at"] <= end_of_day)
            ]
            product_df = product_df[
                (product_df["created_at"] >= start_of_day)
                & (product_df["created_at"] <= end_of_day)
            ]

        # Tratamento de DataFrames vazios APÓS filtragem por data
        # Estes erros serão retornados ao frontend com status 404
        if sale_df.empty:
            raise NotFoundError("No sales found in the specified date range")
        if product_df.empty:
            raise NotFoundError("No products found in the specified date range")


        # --- TOP SELLING PRODUCTS ---
        top_selling_product = (
            sale_df.groupby("product_id")
            .agg({"quantity": "sum"}) # Agrupa e soma a quantidade de produtos vendidos
            .reset_index()
            .sort_values(by="quantity", ascending=False) # Ordena do mais vendido para o menos
        )

        # Mescla com o DataFrame de produtos para obter o nome do produto
        top_selling_product = top_selling_product.merge(
            product_df[["id", "name"]],
            left_on="product_id",
            right_on="id",
            how="left",
        )
        # Preenche NaNs que possam surgir de produtos não encontrados ou dados ausentes
        top_selling_product['name'] = top_selling_product['name'].fillna('Produto Desconhecido')
        top_selling_product['id'] = top_selling_product['id'].fillna('')
        top_selling_product['quantity'] = pd.to_numeric(top_selling_product['quantity'], errors='coerce').fillna(0) # Garante que quantity seja numérico

        top_selling_product = top_selling_product[
            ["id", "name", "quantity"]
        ].head(top_n) # Pega os N produtos mais vendidos
        response["top_selling_product"] = top_selling_product.to_dict(
            orient="records"
        )

        # --- TOP LEAST SOLD PRODUCTS ---
        # Lógica para "menos vendidos": Agrupa, soma, e ordena de forma ascendente
        top_least_sold_products = (
            sale_df.groupby("product_id")
            .agg({"quantity": "sum"})
            .reset_index()
            .sort_values(by="quantity", ascending=True) # <-- CORRIGIDO AQUI: ascending=True
        )

        # Mescla com o DataFrame de produtos para obter o nome
        top_least_sold_products = top_least_sold_products.merge(
            product_df[["id", "name"]],
            left_on="product_id",
            right_on="id",
            how="left",
        )
        # Preenche NaNs
        top_least_sold_products['name'] = top_least_sold_products['name'].fillna('Produto Desconhecido')
        top_least_sold_products['id'] = top_least_sold_products['id'].fillna('')
        top_least_sold_products['quantity'] = pd.to_numeric(top_least_sold_products['quantity'], errors='coerce').fillna(0) # Garante que quantity seja numérico

        top_least_sold_products = top_least_sold_products[
            ["id", "name", "quantity"]
        ].head(top_n) # Pega os N produtos menos vendidos
        response["top_least_sold_products"] = top_least_sold_products.to_dict(
            orient="records"
        )

        # Garante que 'value' (valor da venda) e 'quantity' (quantidade vendida) são numéricos
        sale_df['value'] = pd.to_numeric(sale_df['value'], errors='coerce').fillna(0)
        sale_df['quantity'] = pd.to_numeric(sale_df['quantity'], errors='coerce').fillna(0)

        # --- SALES AMOUNT (RECEITA TOTAL DE VENDAS) ---
        sales_amount: float = sale_df["value"].sum()
        response["sales_amount"] = sales_amount if not pd.isna(sales_amount) else 0.0

        # --- NUMBER OF SALES ---
        number_of_sales: int = sale_df["id"].nunique()
        response["number_of_sales"] = number_of_sales

        # --- NUMBER OF PRODUCTS (ÚNICOS NO PERÍODO) ---
        number_of_products: int = product_df["id"].nunique()
        response["number_of_products"] = number_of_products

        # --- SALES PROFIT (LUCRO BRUTO DAS VENDAS CORRIGIDO E COM PRINTS DE DEPURACAO) ---
        # 1. Mescla sale_df com product_df para obter price_cost e price_sale dos produtos VENDIDOS
        sales_with_product_details = sale_df.merge(
            product_df[["id", "price_cost", "price_sale"]],
            left_on="product_id",
            right_on="id",
            how="left",
            suffixes=('', '_product') # Sufixo para colunas com nomes iguais (id_product)
        )

        # PRINTS DE DEPURACAO
        print(f"DEBUG REPORT: sales_with_product_details HEAD:\n{sales_with_product_details.head()}")
        print(f"DEBUG REPORT: Columns in sales_with_product_details: {sales_with_product_details.columns.tolist()}")

        # Garante que price_cost e price_sale sejam numéricos e preenche NaNs com 0
        sales_with_product_details['price_cost'] = pd.to_numeric(sales_with_product_details['price_cost'], errors='coerce').fillna(0)
        sales_with_product_details['price_sale'] = pd.to_numeric(sales_with_product_details['price_sale'], errors='coerce').fillna(0)

        # PRINTS DE DEPURACAO
        print(f"DEBUG REPORT: price_cost after fillna: {sales_with_product_details['price_cost'].tolist()}")
        print(f"DEBUG REPORT: price_sale after fillna: {sales_with_product_details['price_sale'].tolist()}")
        print(f"DEBUG REPORT: quantity (from sales_with_product_details): {sales_with_product_details['quantity'].tolist()}")


        # Calcula o lucro por item vendido: (preço_venda_do_produto - preço_custo_do_produto) * quantidade_vendida_na_venda
        sales_with_product_details['item_profit'] = (
            (sales_with_product_details['price_sale'] - sales_with_product_details['price_cost'])
            * sales_with_product_details['quantity']
        )
        
        # PRINTS DE DEPURACAO
        print(f"DEBUG REPORT: item_profit calculated: {sales_with_product_details['item_profit'].tolist()}")

        # Soma o lucro de todos os itens vendidos
        sales_profit: float = sales_with_product_details['item_profit'].sum()
        response["sales_profit"] = sales_profit if not pd.isna(sales_profit) else 0.0


        # --- NUMBER OF PRODUCTS SOLD (TOTAL DE ITENS VENDIDOS) ---
        number_of_products_sold: float = sale_df["quantity"].sum()
        response["number_of_products_sold"] = int(number_of_products_sold) if not pd.isna(number_of_products_sold) else 0


        # --- MEAN TICKET (TICKET MÉDIO) ---
        # Certifique-se de que number_of_products_sold é usado corretamente na divisão
        mean_ticket = (
            (sales_amount / response["number_of_products_sold"]) # Usa o número já tratado
            if response["number_of_products_sold"] > 0 # Evita divisão por zero
            else 0.0 # Define como 0.0 se não houver produtos vendidos para evitar NaN
        )
        response["mean_ticket"] = mean_ticket


        # --- TOP SELLER (MAIORES VENDEDORES) ---
        top_seller = (
            sale_df.groupby("user_id").agg({"value": "sum"}).reset_index()
        )
        top_seller['value'] = pd.to_numeric(top_seller['value'], errors='coerce').fillna(0) # Garante valor numérico
        top_seller['user_id'] = top_seller['user_id'].astype(str) # Garante que o ID seja string para mesclagem se necessário

        top_seller = top_seller[["user_id", "value"]].head(top_n) # Seleciona as colunas relevantes e N primeiros
        top_seller.rename(columns={"value": "total_sales", "user_id": "id"}, inplace=True) # Renomeia para o schema

        # Adaptação para o schema ProductReportResponse (SellerResult espera 'id', 'name', 'total_sales')
        # Adiciona um nome genérico, já que não temos o nome real do usuário diretamente aqui
        final_top_seller_list = []
        for index, row in top_seller.iterrows():
            final_top_seller_list.append({
                "id": str(row["id"]),
                "name": f"Usuário {row['id']}", # Usa o ID como parte do nome genérico
                "total_sales": float(row["total_sales"])
            })
        response["top_seller"] = final_top_seller_list

        # Linha de depuração final
        print(f"DEBUG FINAL RESPONSE: {response}")

        # Retorna a resposta validada pelo schema Pydantic
        return ProductReportResponse(**response)