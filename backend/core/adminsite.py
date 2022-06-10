from fastapi import FastAPI
from fastapi_amis_admin.amis.components import App
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite, ReDocsAdmin, DocsAdmin
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request

# 1. 默认后台管理站点,无用户认证与授权系统
# site = AdminSite(settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'))
from core import settings

site = AdminSite(settings=settings)


# 2. 从 fastapi_user_auth 导入安装用户认证与授权系统的后台管理站点
# 使用之前先执行'pip install fastapi_user_auth'安装库
# 参考文档: https://github.com/amisadmin/fastapi_user_auth
# from fastapi_user_auth.site import AuthAdminSite
#
# site = AuthAdminSite(settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'))


# 3. 自定义后台管理站点
class NewAdminSite(AdminSite):
    # 自定义应用模板,复制原模板文件修改,原路径: fastapi_amis_admin/amis/templates/app.html
    template_name = '/templates/new_app.html'

    def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None):
        super().__init__(settings, fastapi, engine)
        # 取消注册默认管理类
        self.unregister_admin(DocsAdmin, ReDocsAdmin)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        # 自定义站点名称,logo信息, 参考: https://baidu.gitee.io/amis/zh-CN/components/app
        app.brandName = 'MyAdminSite'
        app.logo = 'https://baidu.gitee.io/amis/static/logo_408c434.png'
        return app

# site = NewAdminSite(settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'))
