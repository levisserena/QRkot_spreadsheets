from datetime import datetime

from aiogoogle import Aiogoogle
from aiogoogle.models import Response

from app.constants import ConstantGoogle, TableCell, Text
from app.core.config import settings


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создания гугл-таблицы с отчётом на диске сервисного аккаунта."""
    now_date_time = datetime.now().strftime(ConstantGoogle.FORMAT_DATETIME)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'{Text.TITLE_TABLE_GOOGLE}{now_date_time}',
                       'locale': ConstantGoogle.LOCALE},
        'sheets': [{
            'properties': {'sheetType': ConstantGoogle.SHEET_TYPE,
                           'sheetId': ConstantGoogle.SHEET_ID,
                           'title': ConstantGoogle.SHEET_TITLE,
                           'gridProperties': {
                               'rowCount': ConstantGoogle.ROW,
                               'columnCount': ConstantGoogle.COLUMN
                           }}
        }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Выдача прав аккаунту на документы, которые созданы на диске сервисного
    аккаунта"""
    permissions_body = {'type': ConstantGoogle.TYPE_PERMISSION,
                        'role': ConstantGoogle.ROLE_PERMISSION,
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Обновляет данные в гугл-таблице."""
    now_date_time = datetime.now().strftime(ConstantGoogle.FORMAT_DATETIME)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        [TableCell.R1C1, now_date_time],
        [TableCell.R2C1],
        [TableCell.R3C1, TableCell.R3C2, TableCell.R3C3]
    ]
    for project in charity_projects:
        table_values.append([
            str(project.name),
            str(project.delta_date),
            str(project.description)
        ])
    update_body = {
        'majorDimension': ConstantGoogle.MAJOR_DIMENSION,
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=ConstantGoogle.RANGE,
            valueInputOption=ConstantGoogle.VALUE_INPUT_OPTION,
            json=update_body
        )
    )


async def get_spreadsheets(wrapper_services: Aiogoogle) -> Response:
    """Формирует словарь со списком Google-таблиц на диске пользователя.
    Пример:
    ```
    {
      'incompleteSearch': False,
      'kind': 'drive#fileList',
      'files': [{'id': '172NBdowrpNlS0W3VlKpldeYOZoHZr-rLODykB01Zuvc',
        'kind': 'drive#file',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'name': 'QRKot - Отчет от 16:50:19 11/25/24'},
        {'id': '14hveJnbdDAb5dQ3DFS7abwUH8tryssqiy5Ug-n8VB5o',
        'kind': 'drive#file',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'name': 'Отчет от 17:04:52 11/24/24'},
    }
    ```
    Подробнее [тут](
    https://developers.google.com/drive/api/reference/rest/v3/files/list#request-body)
    """
    service = await wrapper_services.discover('drive', 'v3')
    return await wrapper_services.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'
        )
    )


async def delete_spreadsheet(fileId: str, wrapper_services: Aiogoogle) -> None:
    """Удалит Google-таблицу по переданному id."""
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.files.delete(fileId=fileId)
    )
