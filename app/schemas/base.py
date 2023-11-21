from pydantic import BaseModel, Field, conint


MIN_AMOUNT = 1
MIN_INVESTED = 0


class ProjectBase(BaseModel):
    full_amount: conint(ge=MIN_AMOUNT)
    invested_amount: int = Field(default=MIN_INVESTED)
