from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase):

    async def create_donation(
            self,
            donation: DonationCreate,
            session: AsyncSession,
            user: Optional[User] = None
    ):

        from app.validators.base import check_fields
        await check_fields(donation)

        new_donation = donation.dict()
        crete_donation = await super().create(new_donation, session)

        from app.services.investment_function import investment_function
        return await investment_function(crete_donation, session)


donation_crud = CRUDDonation(Donation)
