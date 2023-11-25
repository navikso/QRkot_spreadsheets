from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import MIN_AMOUNT
from app.crud.base import CRUDBase
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import investment
from app.validators.base import check_fields


class CharityProjectService():

    async def check_full_amount(value) -> None:
        if not isinstance(value, int) or value <= 0:
            raise HTTPException(
                status_code=422,
                detail="Требуемая сумма (full_amount) проекта "
                       "должна быть целочисленной и больше 0.",
            )

    async def check_project_name_duplicate(
            charityproject_name: str,
            session: AsyncSession,
    ) -> None:
        charityproject_id = await \
            charity_project_crud.get_charityproject_id_by_name(
                charityproject_name, session
            )

        if charityproject_id is not None:
            raise HTTPException(
                status_code=400,
                detail="Проект с таким именем уже существует!",
            )

    async def check_project_before_create(
            charityproject: CharityProjectCreate,
            session: AsyncSession,
    ):
        await check_fields(charityproject)
        await CharityProjectService.check_project_name_duplicate(
            charityproject.name, session)
        await CharityProjectService.check_full_amount(
            charityproject.full_amount)

    async def create_charityproject(
            self,
            charityproject: CharityProjectCreate,
            session: AsyncSession,
    ):
        await CharityProjectService.check_project_before_create(
            charityproject, session)

        new_project = charityproject.dict()
        project = await CRUDBase(CharityProject).create(new_project, session)

        return await investment(project, session)

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
        charityproject = await CharityProjectService.get_existing_charityproject(
            charityproject_id, session)

        # if obj_in.full_amount and obj_in.full_amount <
        # charityproject.invested_amount:
        #     raise HTTPException(
        #         status_code=400, detail="Сумма сбора не может быть меньше
        #         внесенной!"
        #     )

        if obj_in.invested_amount and obj_in.invested_amount < \
                charityproject.full_amount:
            raise HTTPException(
                status_code=422,
                detail="Сумма сбора не может быть меньше внесенной!"
            )

        if obj_in.invested_amount == MIN_AMOUNT:
            raise HTTPException(
                status_code=422, detail="Сумма сбора не может быть ноль!"
            )

        if charityproject.fully_invested:
            raise HTTPException(
                status_code=400, detail="Закрытый проект нельзя редактировать!"
            )

        if obj_in.name is not None:
            await CharityProjectService.check_project_name_duplicate(
                obj_in.name, session)

        await check_fields(obj_in)
        return charityproject, obj_in

    async def update_charityproject(
            self,
            db_project: CharityProjectDB,
            charityproject: CharityProjectUpdate,
            session: AsyncSession,
    ):
        charityproject, obj_in = await CharityProjectService.get_validated_before_update(
            db_project.id, charityproject, session)

        return await CRUDBase(CharityProject).update(charityproject, obj_in, session)

    async def get_validated_before_delete(
            charityproject_id: int,
            session: AsyncSession,
    ):
        charityproject = await CharityProjectService.get_existing_charityproject(
            charityproject_id, session)

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

    async def remove_charityproject(
            self,
            db_project_id: int,
            session: AsyncSession,
    ):
        db_project = await CharityProjectService.get_validated_before_delete(
            db_project_id, session)

        return await CRUDBase(CharityProject).remove(db_project, session)
