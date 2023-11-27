from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_item_list(
    item: Union[CharityProject, Donation],
    session: AsyncSession,
):
    target = CharityProject if isinstance(item, Donation) else Donation

    sources = await session.execute(
        select(target).where(target.fully_invested.is_(False)).order_by("create_date")
    )
    return sources.scalars().all()


def investment_process(item, sources):
    for source in sources:
        invest_amount = min(
            item.full_amount - item.invested_amount,
            source.full_amount - source.invested_amount,
        )

        item.invested_amount += invest_amount
        source.invested_amount += invest_amount

        if item.full_amount == item.invested_amount:
            item.fully_invested = True
            item.close_date = datetime.now()

        if source.full_amount == source.invested_amount:
            source.fully_invested = True
            source.close_date = datetime.now()

    return item


async def investment(
    item,
    session: AsyncSession,
):
    sources = await get_item_list(item, session)
    target = investment_process(item, sources)

    await session.commit()
    await session.refresh(target)

    return target
