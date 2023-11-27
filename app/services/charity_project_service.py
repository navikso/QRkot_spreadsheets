from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import MIN_AMOUNT
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import investment
from app.validators.base import check_fields


class CharityProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __check_full_amount(self, value) -> None:
        if not isinstance(value, int) or value <= MIN_AMOUNT:
            raise HTTPException(
                status_code=422,
                detail="Требуемая сумма (full_amount) проекта "
                "должна быть целочисленной и больше 0.",
            )

    async def __check_project_name_duplicate(
        self,
        charityproject_name: str,
    ) -> None:
        charityproject_id = await CRUDBase(CharityProject).get_by_attribute(
            "name", charityproject_name, self.session
        )

        if charityproject_id is not None:
            raise HTTPException(
                status_code=400,
                detail="Проект с таким именем уже существует!",
            )

    async def __check_project_before_create(
        self,
        charityproject: CharityProjectCreate,
    ):
        await check_fields(charityproject)
        await self.__check_project_name_duplicate(charityproject.name)
        await self.__check_full_amount(charityproject.full_amount)

    async def create_charityproject(
        self,
        charityproject: CharityProjectCreate,
    ):
        await self.__check_project_before_create(charityproject)

        new_project = charityproject.dict()
        project = await CRUDBase(CharityProject).create(new_project, self.session)

        return await investment(project, self.session)

    async def __get_existing_charityproject(
        self,
        charityproject_id: int,
    ) -> CharityProject:
        charityproject = await CRUDBase(CharityProject).get(
            charityproject_id, self.session
        )
        if not charityproject:
            raise HTTPException(status_code=404, detail="Hе найдена!")

        return charityproject

    async def __get_validated_before_update(
        self,
        charityproject_id: int,
        obj_in: CharityProjectUpdate,
    ):
        charityproject = await self.__get_existing_charityproject(charityproject_id)

        if (
            obj_in.invested_amount
            and obj_in.invested_amount < charityproject.full_amount
        ):
            raise HTTPException(
                status_code=422, detail="Сумма сбора не может быть меньше внесенной!"
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
            await self.__check_project_name_duplicate(obj_in.name)

        await check_fields(obj_in)
        return charityproject, obj_in

    async def update_charityproject(
        self,
        db_project: CharityProjectDB,
        charityproject: CharityProjectUpdate,
    ):
        (
            charityproject,
            obj_in,
        ) = await self.__get_validated_before_update(db_project.id, charityproject)

        return await CRUDBase(CharityProject).update(
            charityproject, obj_in, self.session
        )

    async def __get_validated_before_delete(
        self,
        charityproject_id: int,
    ):
        charityproject = await self.__get_existing_charityproject(charityproject_id)

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
    ):
        db_project = await self.__get_validated_before_delete(db_project_id)

        return await CRUDBase(CharityProject).remove(db_project, self.session)
