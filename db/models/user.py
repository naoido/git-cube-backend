from datetime import datetime

from sqlalchemy import String, Date, Integer
from sqlalchemy.testing.schema import Column

from ..base import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    GitHub_id = Column(String(20), nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())
    deleted_at = Column(Date, nullable=True)
    update_at = Column(Date, nullable=True)