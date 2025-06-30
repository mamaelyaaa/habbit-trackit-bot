from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import db_helper

# Зависимость сессии
SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]
