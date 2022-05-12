import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import update
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.adminsite import site
from apps.blog.models import Article

router = APIRouter(prefix='/articles', tags=['ArticleAPI'])


@router.get('/read/{id}', response_model=Article)
async def read_article(id: int,
                       session: AsyncSession = Depends(site.db.session_factory)):
    stmt = select(Article).where(Article.id == id)
    result = await session.execute(stmt)
    return result.scalar()


@router.get('/update/{id}', response_model=Article)
async def update_article(id: int,
                         session: AsyncSession = Depends(site.db.session_factory)):
    stmt = update(Article).where(Article.id == id).values({'create_time': datetime.datetime.now()})
    result = await session.execute(stmt)
    await session.commit()
    return await read_article(id, session)
