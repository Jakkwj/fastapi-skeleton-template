from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimeCreated:
    created_timestamp = Column(DateTime, default=datetime.now(), index=True, nullable=False)
