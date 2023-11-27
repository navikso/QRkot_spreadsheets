from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.constants import MAX_NAME_LENGTH, MIN_AMOUNT
from app.core.db import Base


class CharityProject(Base):
    name = Column(String(MAX_NAME_LENGTH), nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, default=MIN_AMOUNT)
    invested_amount = Column(Integer, default=MIN_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime)
