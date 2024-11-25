from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ConstantGoogle, Endpoints, Text
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.schemas.google import GoogleBase
from app.services.google_api import (delete_spreadsheet, get_spreadsheets,
                                     set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service),
):
    """Создаст Google-таблицу.
    Вернет список попавших в таблицу благотворительных проектов.
    Только для суперюзеров."""
    charity_projects_fully = (
        await charity_project_crud.get_projects_by_completion_rate(session)
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id,
                                    charity_projects_fully,
                                    wrapper_services)
    return charity_projects_fully


@router.get(
    '/',
    response_model=list[GoogleBase],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_list_report(
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Вернет списком данные о Google-таблицах данного проекта.
    Только для суперюзеров."""
    response = await get_spreadsheets(wrapper_services)
    result = [file_table for file_table in response['files'] if (
        Text.APP_TITLE in file_table['name']
    )]
    for file_table in result:
        file_table['url'] = (
            f'{ConstantGoogle.GET_SPEEEDSHEETS_URL}{file_table["id"]}'
        )
    return result


@router.get(
    Endpoints.GOOGLE_LAST,
    response_model=GoogleBase,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_last_report(
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Вернет списком данные о последней созданной Google-таблице данного
    проекта.
    Только для суперюзеров."""
    list_report = await get_list_report(wrapper_services)
    return [] if not list_report else list_report[0]


@router.delete(
    '/',
    response_model=list[GoogleBase],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_old_reports(
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Удалит старые Google-таблицы данного проекта.
    Только для суперюзеров."""
    list_report = await get_list_report(wrapper_services)
    for spreadsheet in list_report[1:]:
        await delete_spreadsheet(spreadsheet['id'], wrapper_services)
    return list_report[1:]


@router.delete(
    Endpoints.GOOGLE_LAST,
    response_model=GoogleBase,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_last_report(
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Удалит последнюю Google-таблицу данного проекта.
    Только для суперюзеров."""
    last_report = await get_last_report(wrapper_services)
    if last_report:
        await delete_spreadsheet(last_report['id'], wrapper_services)
    return last_report
