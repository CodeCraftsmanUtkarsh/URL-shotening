from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime,timezone
from .db import Base
class URL(Base):
    __tablename__="urls"
    id=Column(Integer,primary_key=True)
    original_url=Column(String,nullable=False)
    short_code=Column(String,unique=True,nullable=False)
    clicks=Column(Integer,default=0)
    created_at=Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
    