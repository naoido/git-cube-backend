from datetime import datetime

from sqlalchemy import String, Date, Integer, Text, ForeignKey
from sqlalchemy.testing.schema import Column

from ..base import Base

class Memo(Base):
    __tablename__ = 'memos'
    memo_id = Column(Integer, primary_key=True)
    GitHub_id = Column(String(20), nullable=False)
    context = Column(Text, nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())

