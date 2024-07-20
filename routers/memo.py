from fastapi import APIRouter, Depends
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update, desc, delete

from db.models import user, memo


memo_router = APIRouter


@memo_router.get("")
async def get_memos(github_id, db : AsyncSession = Depends(get_db)):
    user_ = await db.execute(select(user.User.user_id)
                            .where(user.User.github_id == github_id))
    user_ = user_.fetchall()
    user_id = user_[0].user_id

    result : Result = await db.execute( select (memo.Memo.memo_id, memo.Memo.context)
                                    .where(memo.Memo.user_id == user_id)
    )
    memo_list = result.fetchall()

    memo_list = [item for _ in memo_list for item in _]

    return memo_list

# @memo_router.post("")
# async def regist_memo(github_id, context, db : AsyncSession = Depends(get_db)):
#     user_ = await db.execute(select(user.User.user_id)
#                             .where(user.User.github_id == github_id))
#     user_ = user_.fetchall()
#     user_id = user_[0].user_id

#     get_memo_id = await db.execute(select (memo.Memo.memo_id)
#                                     .order_by(desc(memo.Memo.memo_id))
#                                     .limit(1))
    
#     last_todo_id = get_memo_id.fetchall()

#     memo_dict = {
#         "memo_id" : memo_id, 
#         "user_id" : user_id,
#         "context" : context,
#     }