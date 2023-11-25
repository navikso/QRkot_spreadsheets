from pydantic import BaseModel, Field, conint

from app.constants import MIN_AMOUNT


class ProjectBase(BaseModel):
    full_amount: conint(ge=MIN_AMOUNT)
    invested_amount: int = Field(default=MIN_AMOUNT)
