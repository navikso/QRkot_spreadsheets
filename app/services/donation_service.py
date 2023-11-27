from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate
from app.services.investment import investment
from app.validators.base import check_fields


class DonationService:
    async def create_donation(
        self,
        donation: DonationCreate,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        await check_fields(donation)

        new_donation = donation.dict()
        db_donation = await CRUDBase(Donation).create(new_donation, session)

        return await investment(db_donation, session)
