from datetime import datetime

from sqlalchemy import Date, Integer, ForeignKey
from sqlalchemy.testing.schema import Column

from ..base import Base

from .user import User

class Session(Base):
    __tablename__ = 'session'
    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())

