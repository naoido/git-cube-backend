from fastapi import APIRouter, Depends
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update, desc

from db.models import user, todos

todo_router = APIRouter()

@todo_router.get("")
async def get_todos(github_id, db : AsyncSession = Depends(get_db)):

    result : Result = await db.execute(
        select(todos.Todo.todo_id, todos.Todo.context, todos.Todo.is_success)
        .join(user.User, todos.Todo.user_id == user.User.user_id)
        .where(user.User.github_id == github_id)
        .where(todos.Todo.user_id == user.User.user_id)
    )
    todo_list = result.fetchall()

    todo_list = [item for _ in todo_list for item in _]

    return todo_list

@todo_router.post("")
async def regist_todos(github_id, context, db : AsyncSession = Depends(get_db)):

    user_ = await db.execute(select(user.User.user_id)
                            .where(user.User.github_id == github_id))
    user_ = user_.fetchall()
    user_id = user_[0].user_id

    get_todo_id = await db.execute(select (todos.Todo.todo_id)
                                    .order_by(desc(todos.Todo.todo_id))
                                    .limit(1))
    
    last_todo_id = get_todo_id.fetchall()


    if last_todo_id == []:
        todo_id = 1
    else:
        todo_id = last_todo_id[0].todo_id + 1

    todo_dict = {
        "todo_id": todo_id,
        "user_id": user_id,
        "context": context,
        "is_success": 0,
    }
    todo = todos.Todo(**todo_dict)
    db.add(todo)
    await db.commit()

@todo_router.put("/{todo_id}")
async def change_is_success(github_id, todo_id, db : AsyncSession = Depends(get_db)):
    user_ = await db.execute(select(user.User.user_id)
                            .where(user.User.github_id == github_id))
    user_ = user_.fetchall()
    user_id = user_[0].user_id

    await db.execute(update (todos.Todo.is_success)
                    .where(todos.Todo.user_id == user_id)
                    .where(todos.Todo.todo_id == todo_id))
    await db.commit()

# @todo_router.delete("/{todo_id}")
# async def delete_todo(github_id, todo_id, db:)