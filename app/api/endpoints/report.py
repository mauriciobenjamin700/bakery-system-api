# app/api/endpoints/report.py

from datetime import datetime
from fastapi import APIRouter, Depends, Query # Adicionado Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import admin_permission, get_session
from app.schemas.report import ProductReportResponse # Caminho correto para o Schema
from app.schemas.user import UserResponse # Importado UserResponse
from app.services.report import ReportService 

router = APIRouter(prefix="/report", tags=["report"])


@router.get("/product", response_model=ProductReportResponse) # Adicionado response_model
async def get_product_report(
    start_date: datetime | None = Query(None, description="The start date for the report (e.g., 2024-01-01T00:00:00)"), # Usar Query
    end_date: datetime | None = Query(None, description="The end date for the report (e.g., 2024-12-31T23:59:59)"), # Usar Query
    top_n: int = Query(10, description="The number of top products tocsd include in the report."), # Usar Query
    _: UserResponse = Depends(admin_permission),
    session: AsyncSession = Depends(get_session),
) -> ProductReportResponse:
    """
    # A route to get a report of all products.

    ## Args:
        - start_date (datetime | None): The start date for the report.
        - end_date (datetime | None): The end date for the report.
        - top_n (int): The number of top products to include in the report.
        - session (AsyncSession): The database session.
    ## Returns:
        - dict: A dictionary containing the product report.
    """
    service = ReportService(session)

    # Corrigido: Passar os parâmetros para o serviço
    response = await service.get_product_report(
        start_date=start_date,
        end_date=end_date,
        top_n=top_n
    )

    return response