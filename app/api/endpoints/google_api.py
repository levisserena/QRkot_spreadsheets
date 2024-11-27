from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Endpoints
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.schemas.google import GoogleBase
from app.services.google_api import (delete_last_report, delete_old_reports,
                                     get_response_last_report,
                                     get_response_list_report,
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
    return await get_response_list_report(wrapper_services)


@router.get(
    Endpoints.GOOGLE_LAST,
    response_model=GoogleBase,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_last_report(
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Вернет словарём данные о последней созданной Google-таблице данного
    проекта.
    Только для суперюзеров."""
    return await get_response_last_report(wrapper_services)


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
    return await delete_old_reports(wrapper_services)


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
    return await delete_last_report(wrapper_services)
