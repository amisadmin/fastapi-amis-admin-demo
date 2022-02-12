from fastapi import FastAPI
from starlette.responses import RedirectResponse

from core.adminsite import site

app = FastAPI()

# 导入已注册的后台管理类
from apps import demo
from apps import blog

blog.setup(app)

# 挂载后台管理系统
site.mount_app(app)


# 注册自定义路由
@app.get('/')
async def index():
    return RedirectResponse(url=site.router_path)

# 创建初始化数据库表
@app.on_event("startup")
async def startup():
    await site.create_db_and_tables()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
