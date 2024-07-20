from fastapi import APIRouter, Depends
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

cube_router = APIRouter()

# @cube_router.get("")
