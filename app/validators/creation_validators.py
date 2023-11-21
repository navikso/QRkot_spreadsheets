from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectCreate
from app.validators.base import check_fields


async def check_project_name_duplicate(
    charityproject_name: str,
    session: AsyncSession,
) -> None:
    charityproject_id = await charity_project_crud.get_charityproject_id_by_name(
        charityproject_name, session
    )

    if charityproject_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


async def check_full_amount(value) -> None:
    if not isinstance(value, int) or value <= 0:
        raise HTTPException(
            status_code=422,
            detail="Требуемая сумма (full_amount) проекта "
            "должна быть целочисленной и больше 0.",
        )


async def check_project_before_create(
    charityproject: CharityProjectCreate,
    session: AsyncSession,
):
    await check_fields(charityproject)
    await check_project_name_duplicate(charityproject.name, session)
    await check_full_amount(charityproject.full_amount)

    if charityproject.name is not None:
        await check_project_name_duplicate(charityproject.name, session)
