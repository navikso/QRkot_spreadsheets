from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def read_all_charityproject_from_db(
    session: AsyncSession,
) -> list[CharityProject]:
    db_charityproject = await session.execute(
        select(CharityProject).order_by(CharityProject.create_date)
    )
    return db_charityproject.scalars().all()


async def read_all_donations_from_db(
    session: AsyncSession,
) -> list[Donation]:
    db_donation = await session.execute(
        select(Donation).order_by(Donation.create_date))
    return db_donation.scalars().all()


async def get_validated_before_delete(
    charityproject_id: int,
    session: AsyncSession,
):
    from app.services.charity_project import get_existing_charityproject
    charityproject = await get_existing_charityproject(charityproject_id, session)

    if charityproject.close_date:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )

    if charityproject.invested_amount:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
    return charityproject
