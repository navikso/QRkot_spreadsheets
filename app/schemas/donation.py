from datetime import datetime
from typing import Optional

from pydantic import Field

from app.constants import MIN_AMOUNT, MIN_COMMENT_LENGTH

from .base import ProjectBase


class DonationCreate(ProjectBase):
    comment: Optional[str] = Field(default=None, min_length=MIN_COMMENT_LENGTH)


class DonationDB(DonationCreate):
    id: Optional[int]
    user_id: Optional[int]
    create_date: datetime
    invested_amount: int = Field(default=MIN_AMOUNT)
    fully_invested: int = Field(default=MIN_AMOUNT)

    class Config:
        orm_mode = True
