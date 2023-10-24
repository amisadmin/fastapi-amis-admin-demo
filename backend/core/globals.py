from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite, APIDocsApp, DocsAdmin, ReDocsAdmin
from fastapi_amis_admin.amis.components import App
from sqlalchemy_database import AsyncDatabase, Database
from starlette.requests import Request

from core import settings

# Synchronize Database
sync_db = Database.create(
    settings.database_url,
    session_options={
        "expire_on_commit": False,
    },
)

# Asynchronous Database
async_db = AsyncDatabase.create(
    settings.database_url_async,
    echo=settings.debug,
    session_options={"expire_on_commit": False},
)

site = AdminSite(settings=settings, engine=async_db)

# 1. Default administration site without user authentication and authorization system
# site = AdminSite(settings=settings)

# 2. Import and install user authentication and authorization system from fastapi_user_auth
# Run 'pip install fastapi_user_auth' before using
# Reference Documentation: https://github.com/amisadmin/fastapi_user_auth
# from fastapi_user_auth.site import AuthAdminSite
#
# site = AuthAdminSite(settings=settings)

# 3. Custom Administration Site
class NewAdminSite(AdminSite):
    # Customize application template, copy and modify the original template file, Original path: fastapi_amis_admin/amis/templates/app.html
    template_name = "/templates/new_app.html"

    def __init__(self, settings: Settings, *, fastapi: FastAPI = None, **kwargs):
        super().__init__(settings, fastapi=fastapi, **kwargs)
        app = self.get_admin_or_create(APIDocsApp)
        # Unregister default admin classes
        app.unregister_admin(DocsAdmin, ReDocsAdmin)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        # Customize site name and logo information, Reference: https://baidu.gitee.io/amis/zh-CN/components/app
        app.brandName = "MyAdminSite"
        app.logo = "https://baidu.gitee.io/amis/static/logo_408c434.png"
        return app

# site = NewAdminSite(settings=settings)
