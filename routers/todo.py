from fastapi import APIRouter, Depends
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update, desc, delete

from db.models import user, todos
from routers.session import get_user_id

todo_router = APIRouter()

@todo_router.get("")
async def get_todos(user_id = Depends(get_user_id), db : AsyncSession = Depends(get_db)):

    result : Result = await db.execute(
        select(todos.Todo.todo_id, todos.Todo.context, todos.Todo.is_success)
        .join(user.User, todos.Todo.user_id == user_id)
        .where(todos.Todo.user_id == user.User.user_id)
    )
    items = result.fetchall()

    todo_list = [{"id": item[0], "文章": item[1], "やったかどうか": item[2]} for item in items]

    return todo_list

@todo_router.post("")
async def regist_todos(context, user_id = Depends(get_user_id), db : AsyncSession = Depends(get_db)):


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
async def change_is_success(todo_id, user_id = Depends(get_user_id), db : AsyncSession = Depends(get_db)):
    await db.execute(update (todos.Todo)
                    .where(todos.Todo.user_id == user_id)
                    .where(todos.Todo.todo_id == todo_id)
                    .values(is_success =~ todos.Todo.is_success))
    await db.commit()

@todo_router.delete("/{todo_id}")
async def delete_todo(todo_id, user_id = Depends(get_user_id),db : AsyncSession = Depends(get_db)):
    await db.execute(delete (todos.Todo)
                    .filter (todos.Todo.todo_id == todo_id, todos.Todo.user_id == user_id)
                    )
    await db.commit()