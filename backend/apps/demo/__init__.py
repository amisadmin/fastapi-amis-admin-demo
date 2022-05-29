from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. 导入管理应用
    from . import admin


