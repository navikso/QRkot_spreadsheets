from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tools import (read_all_charityproject_from_db,
                            read_all_donations_from_db)
from app.models import CharityProject, Donation


async def get_item_list(
    item,
    session: AsyncSession,
):
    list = []
    if isinstance(item, CharityProject):
        donation_list = await read_all_donations_from_db(session)
        for donation in donation_list:
            if donation.fully_invested is not True:
                list.append(donation)
        return list

    elif isinstance(item, Donation):
        project_list = await read_all_charityproject_from_db(session)
        for project in project_list:
            if project.fully_invested is not True:
                list.append(project)
        return list


async def investment_function(
    item,
    session: AsyncSession,
):
    list_items = await get_item_list(item, session)

    for list_item in list_items:
        list_item = list_items.pop(0)

        invest_amount = min(
            item.full_amount - item.invested_amount,
            list_item.full_amount - list_item.invested_amount)

        item.invested_amount += invest_amount
        list_item.invested_amount += invest_amount

        if item.full_amount == item.invested_amount:
            item.fully_invested = True
            item.close_date = datetime.now()

        if list_item.full_amount == list_item.invested_amount:
            list_item.fully_invested = True
            list_item.close_date = datetime.now()

        session.add(item)

    await session.commit()
    await session.refresh(item)

    return item
