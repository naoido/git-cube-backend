from datetime import datetime

from sqlalchemy import String, Date, Integer, Text, ForeignKey
from sqlalchemy.testing.schema import Column

from ..base import Base

class Cube(Base):
    __tablename__ = 'cubes'
    cube_id = Column(Integer, primary_key=True)
    GitHub_id = Column(String(20), nullable=False)
    cube_name = Column(String(30))
