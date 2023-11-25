from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.crud.tools import read_all_donations_from_db
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.donation_service import DonationService

router = APIRouter()


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={"invested_amount", "fully_invested", "user_id"},
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await DonationService().create_donation(donation, session, user)


@router.get(
    "/",
    response_model=List[DonationDB],
    response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    all_donations = await read_all_donations_from_db(session)
    return all_donations


@router.get(
    "/my",
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={"invested_amount", "user_id", "fully_invested"},
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    all_donations = await donation_crud.get_by_user(session=session, user=user)
    return all_donations
