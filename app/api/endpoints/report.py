from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import admin_permission, get_session
from app.schemas import ProductReportResponse, UserResponse
from app.services import ReportService

router = APIRouter(prefix="/report", tags=["report"])


@router.get("/product")
async def get_product_report(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    top_n: int = 10,
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

    response = await service.get_product_report()

    return response
