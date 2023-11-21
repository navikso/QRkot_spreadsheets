from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime)
