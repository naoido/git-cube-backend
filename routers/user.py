from fastapi import Depends, APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import update, select

from datetime import timedelta, datetime, timezone
from typing import Optional
from db.models import user



user_router = APIRouter()

