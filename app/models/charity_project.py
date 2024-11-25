from sqlalchemy import CheckConstraint, Column, String, Text
from sqlalchemy.orm import declared_attr

from app.constants import Constant
from app.core.db import Base
from app.models.mixins import InvestmentModelMixin


class CharityProject(InvestmentModelMixin, Base):
    """Благотворительные проекты.

    Проверки name:
    non_empty_name - не позволит создать поле с пустой строкой
    non_extra_space - не допустит пробелы в начале и конце названия
    """

    name = Column(
        String(Constant.LENGTH_NAME_CHARITY_PROJECT),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)

    @declared_attr
    def __table_args__(cls):
        table_args = InvestmentModelMixin.__table_args__ + (
            CheckConstraint('name != ""', name='non_empty_name'),
            CheckConstraint('trim(name) == name', name='non_extra_space'),
        )
        return table_args

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'id={self.id}, '
                f'name={self.name}, '
                f'description={self.description}, '
                f'{super().__repr__()})')
