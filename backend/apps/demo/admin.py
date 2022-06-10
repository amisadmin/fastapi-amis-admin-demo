import datetime
import time
from typing import Dict, Any

from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.amis import TabsModeEnum
from fastapi_amis_admin.amis.components import PageSchema, Page, InputImage
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.enums import IntegerChoices
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from core.adminsite import site


@site.register_admin
class DocsAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label='APIDocs', sort=-100)
    page_schema = PageSchema(label='Docs', icon='fa fa-book')
    src = '/docs'


@site.register_admin
class ReDocsAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label='APIDocs', sort=-100)
    # 设置页面菜单信息
    page_schema = PageSchema(label='Redocs', icon='fa fa-book')

    # 设置跳转链接
    @property
    def src(self):
        return f'{self.app.site.settings.site_url}/redoc'


@site.register_admin
class GitHubLinkAdmin(admin.LinkAdmin):
    # 通过page_schema类属性设置页面菜单信息;
    # PageSchema组件支持属性参考: https://baidu.gitee.io/amis/zh-CN/components/app
    page_schema = PageSchema(label='GitHub', icon='fa fa-github')
    # 设置跳转链接
    link = 'https://github.com/amisadmin/fastapi_amis_admin'


@site.register_admin
class AmisPageApp(admin.AdminApp):
    tabs_mode = TabsModeEnum.radio
    page_schema = PageSchema(label='AmisPage', icon='fa fa-link')

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(HelloWorldPageAdmin, CurrentTimePageAdmin, UserRegFormAdmin)


class HelloWorldPageAdmin(admin.PageAdmin):
    page_schema = PageSchema(label='HelloWorld', icon='fa fa-link')
    # 通过page类属性直接配置页面信息;
    # Page组件支持属性参考: https://baidu.gitee.io/amis/zh-CN/components/page
    page = Page(title='标题', body='Hello World!')


class CurrentTimePageAdmin(admin.PageAdmin):
    page_schema = PageSchema(label='CurrentTime', icon='fa fa-link')

    # 通过get_page类方法实现动态获取页面信息.
    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        page.body = '当前时间是: ' + time.strftime('%Y-%m-%d %H:%M:%S')
        return page


class UserGender(IntegerChoices):
    unknown = 0, '保密'
    man = 1, '男'
    woman = 2, '女'


class UserRegFormAdmin(admin.FormAdmin):
    page_schema = PageSchema(label='UserRegForm', icon='fa fa-link')

    # 创建表单数据模型
    class schema(BaseModel):
        username: str = Field(..., title='用户名')
        password: str = Field(..., title='密码', amis_form_item='input-password')
        birthday: datetime.datetime = Field(None, title='出生日期')
        gender: UserGender = Field(UserGender.unknown, title='性别')
        is_active: bool = Field(True, title='是否激活')
        avatar: str = Field(None, title='头像', max_length=100,
                            amis_form_item=InputImage(maxLength=1, maxSize=2 * 1024 * 1024,
                                                      receiver='post:/admin/file/upload'))

    # 处理表单提交数据
    async def handle(self, request: Request, data: schema, **kwargs) -> BaseApiOut:
        if data.username == 'amisadmin' and data.password == 'amisadmin':
            return BaseApiOut(msg='注册成功!', data={'token': 'xxxxxx'})
        return BaseApiOut(status=-1, msg='用户名或密码错误!')


@site.register_admin
class TemplatePageApp(admin.AdminApp):
    tabs_mode = TabsModeEnum.chrome
    page_schema = PageSchema(label='TemplatePage', icon='fa fa-link')

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(SimpleTemplateAdmin, ElementTemplateAdmin)


class DemoJinja2Admin(admin.TemplateAdmin):
    # group_schema = PageSchema(label='TemplatePage', icon='fa fa-link')
    templates: Jinja2Templates = Jinja2Templates(directory='apps/demo/templates')


class SimpleTemplateAdmin(DemoJinja2Admin):
    page_schema = PageSchema(label='Jinja2', icon='fa fa-link')
    template_name = 'simple.html'

    async def get_page(self, request: Request) -> Dict[str, Any]:
        return {'current_time': datetime.datetime.now()}


class ElementTemplateAdmin(DemoJinja2Admin):
    page_schema = PageSchema(label='ElementUI', icon='fa fa-link')
    template_name = 'element.html'


@site.register_admin
class FastAPIUserAuthAdmin(admin.LinkAdmin):
    group_schema = None
    page_schema = PageSchema(label='FastAPIUserAuth', icon='fa fa-angellist')
    link = 'http://user-auth.demo.amis.work/'


@site.register_admin
class AmisEditorAdmin(admin.IframeAdmin):
    group_schema = None
    page_schema = PageSchema(label='AmisEditorDemo', icon='fa fa-edit', sort=-100)
    src = 'https://aisuda.github.io/amis-editor-demo/'
