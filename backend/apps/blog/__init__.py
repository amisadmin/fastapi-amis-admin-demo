from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. 导入管理应用
    # 2. 注册普通路由
    from . import admin, apis

    app.include_router(apis.router)
