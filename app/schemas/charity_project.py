from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.constants import Constant, Text


class CharityProjectBase(BaseModel):

    @classmethod
    def _validator_field_string(cls, value: str):
        if not value:
            raise ValueError(Text.ERROR_FIELD_EMPTY)
        if value != value.strip():
            raise ValueError(Text.ERROR_FIELD_START_OR_END_SPACE)
        return value


class CharityProjectCreate(CharityProjectBase):

    name: str = Field(
        ...,
        min_length=Constant.NAME_MIN_LENGTH,
        max_length=Constant.NAME_MAX_LENGTH,
        title=Text.NAME_TITLE,
    )
    description: str = Field(..., title=Text.DESCRIPTION_TITLE)
    full_amount: int = Field(
        ..., gt=Constant.FULL_AMOUNT_GT, title=Text.FULL_AMOUNT_TITLE_PROJECT,
    )

    @validator('name')
    def validator_name(cls, value: str):
        return cls._validator_field_string(value)

    @validator('description')
    def validator_description(cls, value: str):
        return cls._validator_field_string(value)


class CharityProjectUpdate(CharityProjectBase):

    name: Optional[str] = Field(
        None,
        min_length=Constant.NAME_MIN_LENGTH,
        max_length=Constant.NAME_MAX_LENGTH,
        title=Text.NAME_TITLE,
    )
    description: Optional[str] = Field(None, title=Text.DESCRIPTION_TITLE)
    full_amount: Optional[int] = Field(
        None, gt=Constant.FULL_AMOUNT_GT, title=Text.FULL_AMOUNT_TITLE_PROJECT
    )

    @validator('name')
    def validator_name(cls, value: str):
        return cls._validator_field_string(value)

    @validator('description')
    def validator_description(cls, value: str):
        return cls._validator_field_string(value)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):

    id: int
    name: str
    description: str
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
