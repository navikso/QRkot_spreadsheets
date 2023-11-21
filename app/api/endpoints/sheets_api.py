from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.sheets_api import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.sheets_api import (get_spreadsheets_from_disk,
                                        delete_spreadsheets_from_disk,
                                        set_user_permissions,
                                        spreadsheets_create,
                                        spreadsheets_update_value)


router = APIRouter()


SHEETS_URL = 'https://docs.google.com/spreadsheets/d/'


@router.post('/',
             dependencies=[Depends(current_superuser)])
async def get_project_progress_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service)
) -> dict[str, str]:
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session)
    spreadsheet_id = await spreadsheets_create(wrapper_service)
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_service)
    return {'Google Sheet URL': SHEETS_URL + spreadsheet_id}


@router.get('/',
            dependencies=[Depends(current_superuser)])
async def get_all_reports(
    wrapper_service: Aiogoogle = Depends(get_service)
) -> list[dict[str, str]]:
    return await get_spreadsheets_from_disk(settings.report_title,
                                            wrapper_service)


@router.delete('/',
               dependencies=[Depends(current_superuser)])
async def clear_all_reports(
    wrapper_service: Aiogoogle = Depends(get_service)
) -> dict[str, str]:
    await delete_spreadsheets_from_disk(wrapper_service)
    return {'message': 'Информация о проектах удалена.'}
