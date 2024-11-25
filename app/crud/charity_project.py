from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Constant
from app.crud.base import CRUDBase
from app.crud.mixins import CRUDFullyInvestedMixin
from app.models import CharityProject


class CRUDCharityProject(CRUDBase, CRUDFullyInvestedMixin):

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        """Возвращает сортированный список со всеми закрытыми проектами по
        количеству времени, которое понадобилось на сбор средств.
        От меньшего к большему."""
        db_project_completion = await session.execute(
            select(self.model).where(
                self.model.fully_invested == Constant.True_
            )
        )
        result = []
        for instance in db_project_completion.scalars().all():
            instance.delta_date = instance.close_date - instance.create_date
            result.append(instance)
        return sorted(result, key=lambda x: x.delta_date)


charity_project_crud = CRUDCharityProject(CharityProject)
