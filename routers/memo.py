from fastapi import APIRouter, Depends
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, desc, delete

from db.models import user, memo
from routers.session import get_user_id


memo_router = APIRouter()

@memo_router.get("/ae")
async def get_testA(user_id = Depends(get_user_id)):
    return user_id

@memo_router.get("")
async def get_memos(user_id = Depends(get_user_id), db : AsyncSession = Depends(get_db)):
    result : Result = await db.execute( select (memo.Memo.memo_id, memo.Memo.context)
                                    .where(memo.Memo.user_id == user_id)
    )
    items = result.fetchall()

    memo_list = [{"id": item[0], "文章": item[1]} for item in items]

    return memo_list

@memo_router.post("")
async def regist_memo(context, user_id = Depends(get_user_id), db : AsyncSession = Depends(get_db)):
    get_memo_id = await db.execute(select (memo.Memo.memo_id)
                                    .order_by(desc(memo.Memo.memo_id))
                                    .limit(1))
    
    last_memo_id = get_memo_id.fetchall()

    if last_memo_id == []:
        memo_id = 1
    else:
        memo_id = last_memo_id[0].memo_id + 1

    memo_dict = {
        "memo_id" : memo_id,
        "user_id" : user_id,
        "context" : context,
    }
    
    mem = memo.Memo(**memo_dict)
    db.add(mem)
    await db.commit()

@memo_router.delete("/{todo_id}")
async def delete_todo(memo_id, user_id = Depends(get_user_id), db : AsyncSession = Depends(get_db)):

    await db.execute(delete (memo.Memo)
                    .filter (memo.Memo.memo_id == memo_id, memo.Memo.user_id == user_id)
                    )
    await db.commit()