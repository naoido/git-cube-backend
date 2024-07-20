from datetime import datetime

from sqlalchemy import String, Date, Integer, Text, Boolean, ForeignKey
from sqlalchemy.testing.schema import Column

from ..base import Base

from .user import User

class Todo(Base):
    __tablename__ = 'todos'
    todo_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    github_id = Column(String(20), nullable=False)
    context = Column(Text, nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())
    is_success = Column(Boolean, nullable=False)


