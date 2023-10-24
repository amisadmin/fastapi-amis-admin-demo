from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. Import the admin application
    from . import admin
