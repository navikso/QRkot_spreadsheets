from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .base import ProjectBase


MIN_LENGTH = 1
MAX_LENGTH = 100


class CharityProjectCreate(ProjectBase):
    name: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(min_length=MIN_LENGTH)


class CharityProjectDB(CharityProjectCreate):
    id: int
    create_date: datetime
    fully_invested: bool = Field(default=False)
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: Optional[int]
    invested_amount: Optional[int]
