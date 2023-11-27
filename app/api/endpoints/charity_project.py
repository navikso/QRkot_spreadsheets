from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
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
    return await CharityProjectService(session).create_charityproject(charityproject)


@router.get(
    "/", response_model=List[CharityProjectDB], response_model_exclude_none=True
)
async def get_all_charityproject(
    session: AsyncSession = Depends(get_async_session),
):
    return await CRUDBase(CharityProject).get_multi(session)


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
    charityproject = await CRUDBase(CharityProject).get(charityproject_id, session)
    return await CharityProjectService(session).update_charityproject(
        charityproject, obj_in
    )


@router.delete(
    "/{charityproject_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
    charityproject_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await CharityProjectService(session).remove_charityproject(charityproject_id)
