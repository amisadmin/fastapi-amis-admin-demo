from core.globals import site
from core.settings import settings
from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.responses import RedirectResponse

app = FastAPI(debug=settings.debug)

# Setup demo application
from apps import demo

demo.setup(app)
# Setup blog application
from apps import blog

blog.setup(app)

# Mount the backend management system
site.mount_app(app)


# Note 1: site.mount_app will by default add site.db's session context middleware.
# If you are using a different database connection, please add it yourself.
# For example:
# from core.globals import sync_db
# app.add_middleware(sync_db.asgi_middleware)
# Note the order in which middleware is registered.

# Note 2: In non-request context, please create your own session,
# such as scheduled tasks, test scripts, etc.
# from core.globals import async_db
# async with async_db():
#     async_db.async_get(...)
#     async_db.session.get(...)
#     # do something

@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    # Run the startup event of the backend management system
    await site.router.startup()


@app.get("/")
async def index():
    return RedirectResponse(url=site.router_path)
