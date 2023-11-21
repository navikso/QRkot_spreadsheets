from datetime import datetime, timedelta
from typing import List, Dict

from aiogoogle import Aiogoogle

from app.core.config import settings


DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


TABLE = {
    'properties': {'sheetId': 0,
                   'title': settings.report_title,
                   'sheetType': 'GRID',
                   'gridProperties': {'rowCount': 100,
                                      'columnCount': 10}}
}

SPREADSHEET = {
    'properties': {
        'title': settings.report_title,
        'locale': 'ru_RU'},
    'sheets': [TABLE]
}

USER_DATA = {'type': 'user', 'role': 'writer', 'emailAddress': settings.email}


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover(
        'drive', settings.google_drive_api_version)
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=USER_DATA,
            fields='id'
        ))


async def spreadsheets_create(
        wrapper_service: Aiogoogle
) -> str:
    service = await wrapper_service.discover(
        'sheets', settings.google_sheets_api_version)
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charityprojects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover(
        'sheets', settings.google_sheets_api_version)
    table_values = [
        ['По состоянию на', datetime.now().strftime(DATE_FORMAT)],
        ['Самые успешные проекты по скорости сбора средств'],
        ['Проект', 'Количество дней сбора', 'Описание']
    ]
    for charityproject in charityprojects:
        new_row = list(charityproject)
        new_row[1] = str(timedelta(days=charityproject[1]))
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=settings.report_range,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def get_spreadsheets_from_disk(
        spreadsheet_title: str,
        wrapper_service: Aiogoogle
) -> List[Dict[str, str]]:
    service = await wrapper_service.discover(
        'drive', settings.google_drive_api_version)
    spreadsheets = await wrapper_service.as_service_account(
        service.files.list(
            q=f'mimeType="application/vnd.google-apps.spreadsheet" and name="{spreadsheet_title}"')
    return spreadsheets['files']


async def delete_spreadsheets_from_disk(
        wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover(
        'drive', settings.google_drive_api_version)
    spreadsheets = await get_spreadsheets_from_disk(settings.report_title,
                                                    wrapper_service)
    for spreadsheet in spreadsheets:
        await wrapper_service.as_service_account(
            service.files.delete(fileId=spreadsheet['id']))
