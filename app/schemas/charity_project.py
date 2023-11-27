from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.constants import MAX_NAME_LENGTH, MIN_DESCR_LENGTH, MIN_NAME_LENGTH

from .base import ProjectBase


class CharityProjectCreate(ProjectBase):
    name: str = Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(min_length=MIN_DESCR_LENGTH)


class CharityProjectDB(CharityProjectCreate):
    id: int
    create_date: datetime
    fully_invested: bool = Field(default=False)
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    name: str = Field(None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(None, min_length=MIN_DESCR_LENGTH)
    full_amount: Optional[int]
    invested_amount: Optional[int]
