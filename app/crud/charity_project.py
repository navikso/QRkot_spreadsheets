from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityproject(CRUDBase):
    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> List[Tuple[str]]:
        query = (
            select(
                [
                    self.model.name,
                    (
                        func.julianday(self.model.close_date
                                       ) - func.julianday(self.model.create_date)
                    ).label("fаster"),
                    self.model.description,
                ]
            )
            .where(self.model.fully_invested is True)
            .order_by("fаster")
        )
        charityprojects = await session.execute(query)

        return charityprojects.all()


charity_project_crud = CRUDCharityproject(CharityProject)
