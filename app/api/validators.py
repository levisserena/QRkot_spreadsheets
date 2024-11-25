from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Text
from app.crud import charity_project_crud
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_object_exists(
    model_crud: CRUDBase,
    object_id: int,
    session: AsyncSession,
    message: str = Text.ERROR_NOT_FOUND
):
    """Проверит наличие и вернет объект из таблицы по id."""
    object_model = await model_crud.get(object_id, session)
    if object_model is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=message,
        )
    return object_model


async def check_name_duplicate(
    charity_project_name: str, session: AsyncSession,
) -> None:
    """Проверка на уникальность названия благотворительного проекта."""
    charity_project = await charity_project_crud.get_by_attribute(
        'name', charity_project_name, session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Text.ERROR_UNIQUE_NAME,
        )


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверит наличие и вернет благотворительный объект из таблицы по id."""
    return await check_object_exists(
        charity_project_crud, project_id, session, Text.ERROR_NOT_PROJECT
    )


def check_fully_invested(project_charity: CharityProject) -> None:
    """Проверит, что изменяемый благотворительного проект не закрыт."""
    if project_charity.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Text.ERROR_FULLY_INVESTED
        )


def check_full_amount_ge_invested_amount(
    project_charity: CharityProject, object_in: CharityProjectUpdate
) -> None:
    """Проверит, что при изменение благотворительного проекта его требуемая
    сумма full_amount больше чем уже внесенные средства invested_amount."""
    if object_in.full_amount is not None and (
        project_charity.invested_amount > object_in.full_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Text.ERROR_FULL_AMOUNT_GE_INVESTED_AMOUNT
        )


def check_can_remove_charity_project(charity_project: CharityProject) -> None:
    """Проверит, перед удалением, не внесены ли средства в проект."""
    if charity_project.invested_amount or charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Text.ERROR_REMOVE_CHARITY_PROJECT
        )
