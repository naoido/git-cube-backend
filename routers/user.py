from fastapi import Depends, APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import update, select
import uuid
from datetime import timedelta, datetime, timezone
from typing import Optional
from db.models import user, session
import json


user_router = APIRouter()

@user_router.post("")
async def regist_user(github_id, user_id, db : AsyncSession = Depends(get_db)):
    
    user_dict = {
        "user_id" : user_id,
        "github_id" : github_id,
        "contributes": 0,
    }

@user_router.post("/sessions")
async def create_sessions(user_id, db: AsyncSession = Depends(get_db)):

    session_id = str(uuid())

    session_dict = {
        "session_id":session_id,
        "user_id":id,
    }
    
    user_sessions = session.Session(**session_dict)
    db.add(user_sessions)
    await db.commit()

    response_content = {"session_id":"success"}
    response = Response(content=json.dumps(response_content), media_type="application/json")
    JST = timezone(timedelta(hours=+9))

    expires_in = timedelta(days=1)
    expires = datetime.now(JST) + expires_in
    expires_utc = expires.astimezone(timezone.utc)

    response.set_cookie(
        'session_id', session_id, expires=expires_utc, httponly=True, secure=True
    )
    return response
