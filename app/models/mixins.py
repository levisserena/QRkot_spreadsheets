from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Integer

from app.constants import Constant


class InvestmentModelMixin:

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer, nullable=False, default=Constant.START_INVESTED_AMOUNT_STR
    )
    fully_invested = Column(
        Integer, nullable=False, default=Constant.False_
    )
    create_date = Column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )
    close_date = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='give_your_money'),
        CheckConstraint('invested_amount >= 0', name='debt_free'),
        CheckConstraint('full_amount >= invested_amount', name='I_love_money'),
    )

    def __repr__(self):
        return (f'full_amount={self.full_amount}, '
                f'invested_amount={self.invested_amount}, '
                f'fully_invested={self.fully_invested}, '
                f'create_date={self.create_date}, '
                f'close_date={self.close_date}')