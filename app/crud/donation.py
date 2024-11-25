from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.mixins import CRUDFullyInvestedMixin
from app.models import Donation, User


class CRUDDonation(CRUDBase, CRUDFullyInvestedMixin):

    async def get_multi_user(self, user: User, session: AsyncSession):
        """Возвращает из таблицы все пожертвования пользователя."""
        db_obj_user = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return db_obj_user.scalars().all()


donation_crud = CRUDDonation(Donation)
