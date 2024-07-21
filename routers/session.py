from fastapi import Request, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import session
from db.db import get_db



async def get_user_id(request: Request, db : AsyncSession = Depends(get_db)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=403, detail="Session ID is missing")
    
    user_id = await db.execute(select (session.Session.user_id)
                            .where(session.Session.session_id == session_id)
                            .limit(1))
    
    user_id = user_id.fetchall()

    get_user_id = [item for _ in user_id for item in _]

    return get_user_id
    