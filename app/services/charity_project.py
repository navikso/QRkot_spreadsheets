from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from app.validators.creation_validators import check_project_name_duplicate
from app.validators.base import check_fields


MIN_AMOUNT = 0


async def get_existing_charityproject(
    charityproject_id: int,
    session: AsyncSession,
) -> CharityProject:
    charityproject = await charity_project_crud.get_charityproject_by_id(
        charityproject_id, session
    )
    if not charityproject:
        raise HTTPException(status_code=404, detail="Hе найдена!")

    return charityproject


async def get_validated_before_update(
    charityproject_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
):
    charityproject = await get_existing_charityproject(charityproject_id, session)

    if obj_in.full_amount and obj_in.full_amount < charityproject.invested_amount:
        raise HTTPException(
            status_code=400, detail="Сумма сбора не может уменьшаться!"
        )

    if obj_in.full_amount == MIN_AMOUNT:
        raise HTTPException(
            status_code=400, detail="Сумма сбора не может быть ноль!"
        )

    if charityproject.fully_invested:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!"
        )

    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)

    await check_fields(obj_in)
    return charityproject, obj_in


async def get_validated_before_delete(
    charityproject_id: int,
    session: AsyncSession,
):
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
