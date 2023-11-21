from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)

CHARITYPROJECT_LEN = 1


class CRUDCharityproject(CRUDBase):

    async def create_charityproject(
            self,
            charityproject: CharityProjectCreate,
            session: AsyncSession,
    ):
        from app.validators.creation_validators import check_project_before_create
        await check_project_before_create(charityproject, session)

        new_project = charityproject.dict()
        project = await super().create(new_project, session)

        from app.services.investment_function import investment_function
        return await investment_function(project, session)

    async def update_charityproject(
            self,
            db_project: CharityProjectDB,
            charityproject: CharityProjectUpdate,
            session: AsyncSession,
    ):

        from app.services.charity_project import get_validated_before_update
        charityproject, obj_in = await get_validated_before_update(
            db_project.id, charityproject, session)

        return await super().update(charityproject, obj_in, session)

    async def remove_charityproject(
            self,
            db_project_id: int,
            session: AsyncSession,
    ):
        from app.services.charity_project import get_validated_before_delete
        db_project = await get_validated_before_delete(db_project_id, session)

        return await super().remove(db_project, session)

    async def get_charityproject_by_id(
        self,
        charityproject_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_charityproject = await session.get(CharityProject, charityproject_id)
        return db_charityproject

    async def get_charityproject_id_by_name(
        self,
        charityproject_name: str,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_charityproject = list(
            await session.execute(
                select(CharityProject).filter(
                    CharityProject.name == charityproject_name
                )
            )
        )

        if len(db_charityproject) == CHARITYPROJECT_LEN:
            return db_charityproject[0][0].id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[tuple[str]]:
        query = select([
            self.model.name,
            (func.julianday(self.model.close_date) -
             func.julianday(self.model.create_date)).label('fаster'),
            self.model.description
        ]).where(self.model.fully_invested == True).order_by('fаster')
        charityprojects = await session.execute(query)
        return charityprojects.all()


charity_project_crud = CRUDCharityproject(CharityProject)
