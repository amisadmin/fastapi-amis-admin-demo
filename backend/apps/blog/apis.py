import datetime
from typing import List

from core.globals import site
from fastapi import APIRouter
from fastapi_amis_admin.globals.deps import AsyncSess
from sqlalchemy import insert, select

from apps.blog.models import Article, ArticleStatus

router = APIRouter(prefix="/articles", tags=["ArticleAPI"])

# Way 1: Use FastAPI dependencies to handle sessions automatically. (Recommended)
# Note: FastAPI will cache dependencies for the same request.
# Be cautious when using synchronous sessions in asynchronous methods.
@router.get("/read/{id}", response_model=Article, summary="Read article")
async def read_article(id: int, session: AsyncSess):
    return await session.get(Article, id)


@router.get("/update/{id}", response_model=Article, summary="Update article")
async def update_article(id: int, session: AsyncSess):
    article = await session.get(Article, id)
    if article:
        article.create_time = datetime.datetime.now()
        await session.flush()
    return article

# Way 2: Use the shortcut functions provided by `sqlalchemy-database`.
@router.get("/read2/{id}", response_model=Article, summary="Read article")
async def read_article2(id: int):
    article = await site.db.async_get(Article, id)
    return article


@router.put("/update2/{id}", response_model=Article, summary="Update article")
async def update_article2(id: int):
    article = await site.db.async_get(Article, id)
    if article:
        article.create_time = datetime.datetime.now()
        await site.db.async_flush()
    return article


@router.post("/create2/", response_model=int, summary="Create article")
async def create_article2(data: Article):
    stmt = insert(Article).values(data.dict(exclude={"id"}))
    result = await site.db.async_execute(stmt)
    return result.lastrowid


@router.get("/list2", response_model=List[Article], summary="List articles")
async def list_article2():
    stmt = select(Article).where(Article.status == ArticleStatus.published.value).limit(10).order_by(Article.create_time)
    result = await site.db.async_scalars(stmt)
    return result.all()

# Way 3: Register a middleware to handle session automatically on each request.
@router.get("/read3/{id}", response_model=Article, summary="Read article")
async def read_article3(id: int):
    article = await site.db.session.get(Article, id)
    return article


@router.put("/update3/{id}", response_model=Article, summary="Update article")
async def update_article3(id: int):
    article = await site.db.session.get(Article, id)
    if article:
        article.create_time = datetime.datetime.now()
        await site.db.session.flush()
    return article


@router.post("/create3/", response_model=int, summary="Create article")
async def create_article3(data: Article):
    stmt = insert(Article).values(data.dict(exclude={"id"}))
    result = await site.db.session.execute(stmt)
    return result.lastrowid


@router.get("/list3", response_model=List[Article], summary="List articles")
async def list_article3():
    stmt = select(Article).where(Article.status == ArticleStatus.published.value).limit(10).order_by(Article.create_time)
    result = await site.db.session.scalars(stmt)
    return result.all()
