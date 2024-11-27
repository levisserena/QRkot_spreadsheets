from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_can_remove_charity_project,
                                check_charity_project_exists,
                                check_full_amount_ge_invested_amount,
                                check_fully_invested, check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment_process import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создание нового благотворительного проекта. Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    update_donation = await donation_crud.get_fully_invested_is_false(session)
    investment_process(new_charity_project, update_donation)
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Выводит список всех благотворительных проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    object_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Частичное изменение благотворительного проекта.
    Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    check_fully_invested(charity_project)
    if object_in.name is not None:
        await check_name_duplicate(object_in.name, session)
    check_full_amount_ge_invested_amount(charity_project, object_in)
    return await charity_project_crud.update(
        charity_project, object_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
    средства, его можно только закрыть. Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    check_can_remove_charity_project(charity_project)
    return await charity_project_crud.remove(
        charity_project, session
    )
