from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import employer_permission, get_session
from app.schemas import Message, SaleNoteRequest, SaleNoteResponse
from app.schemas.user import UserResponse
from app.services import SaleService

router = APIRouter(prefix="/sale", tags=["Sale"])


@router.post("/", status_code=201)
async def create_sale(
    request: SaleNoteRequest,
    session: AsyncSession = Depends(get_session),
    _: UserResponse = Depends(employer_permission),
) -> SaleNoteResponse:
    """
    # A route to create a sale.

    ## Args:
        - request (SaleNoteRequest): The request object containing sale data.
        - session (AsyncSession): The database session.
        - _ (UserResponse): The user making the request.
    ## Returns:
        - SaleNoteResponse: The response object containing the added sale data.
    """
    service = SaleService(session)
    response = await service.add(request)
    return response


@router.get("/code/{sale_code}", status_code=200)
async def get_sale_note(
    sale_code: str,
    session: AsyncSession = Depends(get_session),
    _: UserResponse = Depends(employer_permission),
) -> SaleNoteResponse:
    """
    # A route to get a sale note by its code.

    ## Args:
        - sale_code (str): The code of the sale note.
        - session (AsyncSession): The database session.
        - _ (UserResponse): The user making the request.
    ## Returns:
        - SaleNoteResponse: The response object containing the sale note data.
    """
    service = SaleService(session)
    response = await service.get_sale_note_by_sale_code(sale_code)
    return response


@router.put("/confirm/{sale_code}", status_code=200)
async def confirm_sale_note(
    sale_code: str,
    session: AsyncSession = Depends(get_session),
    _: UserResponse = Depends(employer_permission),
) -> SaleNoteResponse:
    """
    # A route to confirm a sale note by its code.

    ## Args:
        - sale_code (str): The code of the sale note.
        - session (AsyncSession): The database session.
        - _ (UserResponse): The user making the request.
    ## Returns:
        - SaleNoteResponse: The response object containing the confirmed sale note data.
    """
    service = SaleService(session)
    response = await service.confirm_sale(sale_code)
    return response


@router.delete("/cancel/{sale_code}", status_code=200)
async def cancel_sale_note(
    sale_code: str,
    session: AsyncSession = Depends(get_session),
    _: UserResponse = Depends(employer_permission),
) -> Message:
    """
    # A route to cancel a sale note by its code.

    ## Args:
        - sale_code (str): The code of the sale note.
        - session (AsyncSession): The database session.
        - _ (UserResponse): The user making the request.
    ## Returns:
        - SaleNoteResponse: The response object containing the canceled sale note data.
    """
    service = SaleService(session)
    response = await service.cancel_sale_note(sale_code)
    return response
