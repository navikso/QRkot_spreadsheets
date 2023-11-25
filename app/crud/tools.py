from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def read_all_charityproject_from_db(
    session: AsyncSession,
) -> List[CharityProject]:
    db_charityproject = await session.execute(
        select(CharityProject).order_by(CharityProject.create_date)
    )
    return db_charityproject.scalars().all()


async def read_all_donations_from_db(
    session: AsyncSession,
) -> List[Donation]:
    db_donation = await session.execute(
        select(Donation).order_by(Donation.create_date))
    return db_donation.scalars().all()
