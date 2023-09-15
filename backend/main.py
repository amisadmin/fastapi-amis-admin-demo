from core.globals import site
from core.settings import settings
from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.responses import RedirectResponse

app = FastAPI(debug=settings.debug)

# 安装应用demo
from apps import demo

demo.setup(app)
# 安装应用blog
from apps import blog

blog.setup(app)

# 挂载后台管理系统
site.mount_app(app)


# 注意1: site.mount_app会默认添加site.db的session会话上下文中间件,如果你使用了其他的数据库连接,请自行添加.例如:
# from core.globals import sync_db
# app.add_middleware(sync_db.asgi_middleware) # 注意中间件的注册顺序.

# 注意2: 非请求上下文中,请自行创建session会话,例如:定时任务,测试脚本等.
# from core.globals import async_db
# async with async_db():
#     async_db.async_get(...)
#     async_db.session.get(...)
#     # do something


@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    # 运行后台管理系统启动事件
    await site.router.startup()


@app.get("/")
async def index():
    return RedirectResponse(url=site.router_path)
