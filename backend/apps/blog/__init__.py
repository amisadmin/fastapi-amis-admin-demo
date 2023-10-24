from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. Import the admin application
    # 2. Register normal routes
    from . import admin, apis, events

    app.include_router(apis.router)
