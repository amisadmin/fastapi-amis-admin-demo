from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. 导入已注册的后台管理类
    from . import admin
    # 2. 注册普通路由
    from .apis import router
    app.include_router(router)
