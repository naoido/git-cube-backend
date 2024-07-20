from fastapi import APIRouter, Depends
from db.db import get_db 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from db.models import user, cube 
from sqlalchemy import select, delete, update, null, desc, func

cube_router = APIRouter()


@cube_router.get("/cube")
async def get_cube(user_id, cube_id):

    result: Result = await db.execute(
        select(user.User.user_id)
        .join(user.User.user_id == cube.Collect_cube.user_id)
        .join(cube.Collect_cube.cube_id == cube.Cube.cube_id)
        .where(user.User.user_id == user_id)
    )
    
    user_info = result.fetchone()
    
    return user_info