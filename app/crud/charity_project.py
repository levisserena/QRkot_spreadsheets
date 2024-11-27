from datetime import timedelta

from sqlalchemy import extract, select
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
            select(
                self.model,
                (extract('epoch', self.model.close_date) - extract(
                    'epoch', self.model.create_date)).label('delta_date')
            ).where(
                self.model.fully_invested == Constant.True_
            ).order_by('delta_date')
        )
        result = []
        for project in db_project_completion.all():
            project[0].delta_date = timedelta(seconds=project[1])
            result.append(project[0])
        return result


charity_project_crud = CRUDCharityProject(CharityProject)
