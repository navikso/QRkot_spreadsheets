from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import ProjectBase


MIN_INVESTED = 0
MIN_LENGTH = 1


class DonationCreate(ProjectBase):
    comment: Optional[str] = Field(default=None, min_length=MIN_LENGTH)


class DonationDB(DonationCreate):
    id: Optional[int]
    user_id: Optional[int]
    create_date: datetime
    invested_amount: int = Field(default=MIN_INVESTED)
    fully_invested: int = Field(default=MIN_INVESTED)

    class Config:
        orm_mode = True
