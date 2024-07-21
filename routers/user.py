import json
import uuid
from datetime import datetime, timedelta, timezone

import requests
from db.db import get_db
from db.models import session, user
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from routers.session import get_user_id
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter()

@user_router.post("")
async def regist_user(github_id, user_id, db : AsyncSession = Depends(get_db)):
    
    user_dict = {
        "user_id" : user_id,
        "github_id" : github_id,
        "contributes": 0,
    }

    use = user.User(**user_dict)
    db.add(use)
    await db.commit()

@user_router.get("/repo")
async def get_repo(user_id = Depends(get_user_id), db : AsyncSession = Depends(get_db)):

    url_list = db.execute(select (user.User.repo_url)
                    .where (user.User.user_id == user_id)
                    .limit(1))
    ur_ = url_list.fetchall()
    url  = [item for _ in ur_ for item in _]
    text = requests.get(url)

    list = []

    a = text.json()

    for i in range(len(a)):
        tmp = {"repo_name":a[i]["name"]}, {"id":a[i]["id"]}
        list.append(tmp)
    
    return list

@user_router.post("/sessions")
async def create_sessions(user_id, db: AsyncSession = Depends(get_db)):

    session_id = str(uuid.uuid4())

    session_dict = {
        "session_id":session_id,
        "user_id":user_id,
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
