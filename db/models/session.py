from datetime import datetime

from sqlalchemy import Date, Integer, ForeignKey, String
from sqlalchemy.testing.schema import Column

from ..base import Base

from .user import User

class Session(Base):
    __tablename__ = 'user_sessions'
    session_id = Column(String(30), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())
