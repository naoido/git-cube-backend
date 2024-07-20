from datetime import datetime

from sqlalchemy import String, Date, Integer, Text, ForeignKey
from sqlalchemy.testing.schema import Column

from ..base import Base

from .user import User

class Cube(Base):
    __tablename__ = 'cubes'
    cube_id = Column(Integer, primary_key=True)
    cube_name = Column(String(30), nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())

class Collet_cube(Base):
    __table_name__ = 'collect_cubes'
    id = Column(Integer, primary_key=True)
    cube_id = Column(Integer, ForeignKey(Cube.cube_id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.user_id), nulllable=False)
    created_at = Column(Date, nullable=False, default=datetime.now())