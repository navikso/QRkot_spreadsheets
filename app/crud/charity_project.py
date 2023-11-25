from typing import List, Optional, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityproject(CRUDBase):

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
        if db_charityproject:
            return db_charityproject[0][0].id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> List[Tuple[str]]:
        query = select([
            self.model.name,
            (func.julianday(self.model.close_date) -
             func.julianday(self.model.create_date)).label('fаster'),
            self.model.description
        ]).where(self.model.fully_invested == True).order_by('fаster')
        charityprojects = await session.execute(query)
        return charityprojects.all()


charity_project_crud = CRUDCharityproject(CharityProject)
