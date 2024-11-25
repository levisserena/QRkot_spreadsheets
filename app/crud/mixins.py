from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Constant


class CRUDFullyInvestedMixin:
    """Добавляет метод поиска не полностью инвестированных объектов."""

    async def get_fully_invested_is_false(self, session: AsyncSession):
        """Возвращает не полностью инвестированные объекты."""
        db_obj_fully_invested_is_false = await session.execute(
            select(self.model).where(
                self.model.fully_invested == Constant.False_
            )
        )
        return db_obj_fully_invested_is_false.scalars().all()
