from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas.donation import DonationAdminDB, DonationCreate, DonationDB
from app.services.investment_process import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Создание нового пожертвования. Только для авторизованного
    пользователя."""
    new_donation = await donation_crud.create(donation, session, user)
    update_charity_project = (
        await charity_project_crud.get_fully_invested_is_false(session)
    )
    result_investment = investment_process(
        new_donation, update_charity_project
    )
    session.add_all(result_investment)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Выводит список всех пожертвований. Только для суперюзера."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB]
)
async def get_all_donations_user(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех пожертвований авторизованного пользователя."""
    return await donation_crud.get_multi_user(user, session)
