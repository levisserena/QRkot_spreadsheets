from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.mixins import InvestmentModelMixin


class Donation(InvestmentModelMixin, Base):
    """Пожертвования."""

    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'id={self.id}, '
                f'user_id={self.user_id}, '
                f'comment={self.comment}, '
                f'{super().__repr__()})')
