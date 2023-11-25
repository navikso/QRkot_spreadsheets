from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.tools import read_all_charityproject_from_db
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.charity_project_service import CharityProjectService


router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
    charityproject: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await CharityProjectService().create_charityproject(
        charityproject, session)


@router.get(
    "/", response_model=List[CharityProjectDB], response_model_exclude_none=True
)
async def get_all_charityproject(
    session: AsyncSession = Depends(get_async_session),
):
    return await read_all_charityproject_from_db(session)


@router.patch(
    "/{charityproject_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
    charityproject_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charityproject = await charity_project_crud.get_charityproject_by_id(
        charityproject_id, session)
    return await CharityProjectService().update_charityproject(
        charityproject, obj_in, session)


@router.delete(
    "/{charityproject_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
    charityproject_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await CharityProjectService().remove_charityproject(
        charityproject_id, session)
