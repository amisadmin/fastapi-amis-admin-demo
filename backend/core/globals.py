from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite, APIDocsApp, DocsAdmin, ReDocsAdmin
from fastapi_amis_admin.amis.components import App
from sqlalchemy_database import AsyncDatabase, Database
from starlette.requests import Request

from core import settings

# 同步数据库.
sync_db = Database.create(
    settings.database_url,
    session_options={
        "expire_on_commit": False,
    },
)

# 异步数据库
async_db = AsyncDatabase.create(
    settings.database_url_async,
    echo=settings.debug,
    session_options={"expire_on_commit": False},
)

site = AdminSite(settings=settings, engine=async_db)


# 1. 默认后台管理站点,无用户认证与授权系统
# site = AdminSite(settings=settings)

# 2. 从 fastapi_user_auth 导入安装用户认证与授权系统的后台管理站点
# 使用之前先执行'pip install fastapi_user_auth'安装库
# 参考文档: https://github.com/amisadmin/fastapi_user_auth
# from fastapi_user_auth.site import AuthAdminSite
#
# site = AuthAdminSite(settings=settings)


# 3. 自定义后台管理站点
class NewAdminSite(AdminSite):
    # 自定义应用模板,复制原模板文件修改,原路径: fastapi_amis_admin/amis/templates/app.html
    template_name = "/templates/new_app.html"

    def __init__(self, settings: Settings, *, fastapi: FastAPI = None, **kwargs):
        super().__init__(settings, fastapi=fastapi, **kwargs)
        app = self.get_admin_or_create(APIDocsApp)
        # 取消注册默认管理类
        app.unregister_admin(DocsAdmin, ReDocsAdmin)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        # 自定义站点名称,logo信息, 参考: https://baidu.gitee.io/amis/zh-CN/components/app
        app.brandName = "MyAdminSite"
        app.logo = "https://baidu.gitee.io/amis/static/logo_408c434.png"
        return app


# site = NewAdminSite(settings=settings)
