from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.constants import Constant, Text


class DonationBase(BaseModel):

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):

    full_amount: int = Field(
        ..., gt=Constant.FULL_AMOUNT_GT, title=Text.FULL_AMOUNT_TITLE_DONATION,
    )
    comment: str = Field(None, title=Text.COMMENT_TITLE)


class DonationDB(BaseModel):

    id: int
    create_date: datetime
    full_amount: int
    comment: Optional[str]

    class Config:
        orm_mode = True


class DonationAdminDB(DonationDB):

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
