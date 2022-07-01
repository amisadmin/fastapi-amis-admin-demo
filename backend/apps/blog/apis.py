import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import update, select, insert, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.blog.models import Article, ArticleStatus
from core.adminsite import site

router = APIRouter(prefix='/articles', tags=['ArticleAPI'])


# 方式一: 通过FastAPI依赖自动处理,获取session. 特点:
# 1.同一个请求FastAPI会缓存依赖,对于多级依赖,同一个请求多次使用session对象,会减少session的获取成本.
# 2.如果`site.db`使用的是`AsyncDatabase`异步连接,则获取的是`AsyncSession`.
# 3.如果`site.db`使用的是`Database`同步连接,则获取的是`Session`.
#   2.1.同步Session可以充分利用`sqlalchemy`模型懒加载的特性.
#   2.2.注意不要在异步方法中使用同步Session,否则可能堵塞异步循环.
@router.get('/read/{id}', response_model=Article, summary='读取文章')
async def read_article(
        id: int,
        session: AsyncSession = Depends(site.db.session_generator)
):
    return await session.get(Article, id)


@router.get('/update/{id}', response_model=Article, summary='更新文章')
async def update_article(
        id: int,
        session: AsyncSession = Depends(site.db.session_generator)
):
    stmt = update(Article).where(Article.id == id).values({'create_time': datetime.datetime.now()})
    result = await session.execute(stmt)
    await session.commit()
    return await read_article(id, session)


# 方式二: 通过`sqlalchemy-database`提供的快捷函数.特点:
# 1.每次执行数据库操作都获取一个新的session.
#   1.1.如果需要多次使用同一个session,可以通过封装一个函数, 使用`run_sync`方法,减少session获取成本.
# 2.通过`async_`前缀方法,可以不用区分数据库连接是同步连接,还是异步连接.
#   2.1对于特定的项目,在能确定数据库连接是同步或异步的情况下,建议明确调用对应的方法.
#   2.2如果开发一个python包,供其他人使用不能确定连接是同步或异步,应该统一使用`async_`前缀方法.

@router.get('/read2/{id}', response_model=Article, summary='读取文章')
async def read_article2(id: int):
    return await site.db.async_get(Article, id)


@router.put('/update2/{id}', response_model=Article, summary='更新文章')
async def update_article2(id: int):
    stmt = update(Article).where(Article.id == id).values({'create_time': datetime.datetime.now()})
    result = await site.db.async_execute(stmt)
    return await read_article2(id)


@router.post('/create2/', response_model=int, summary='新增文章')
async def create_article2(data: Article):
    # 新增数据模型根据实际情况自己定义
    stmt = insert(Article).values(data.dict(exclude={'id'}))
    result = await site.db.async_execute(stmt)
    return result.lastrowid


@router.delete('/delete2/{id}', response_model=int, summary='删除文章')
async def delete_article2(id: int):
    stmt = delete(Article).where(Article.id == id)
    result = await site.db.async_execute(stmt)
    return result.rowcount


@router.get('/list', response_model=List[Article], summary='读取文章列表')
async def list_article2():
    # 通用的查询表达式可以写在ORM模型,提供一个方法调用.
    stmt = select(Article).where(Article.status == ArticleStatus.published.value).limit(10).order_by(Article.create_time)
    return await site.db.async_scalars_all(stmt)
