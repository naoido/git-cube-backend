from fastapi import APIRouter, Depends
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update

from db.models import user, todos

todo_router = APIRouter()

@todo_router.get("")
async def get_todos(github_id, db : AsyncSession = Depends(get_db)):

    result : Result = await db.execute(
        select(todos.Todo.context)
        .join(user.User, todos.Todo.user_id == user.User.user_id)
        .where(user.User.github_id == github_id)
        .where(todos.Todo.user_id == user.User.user_id)
    )
    todo_list = result.fetchall()

    todo_list = [item for _ in todo_list for item in _]

    return todo_list

# @todo_router.post("")
# async def regist_todos(user_id, db : AsyncSession = Depends(get_db)):