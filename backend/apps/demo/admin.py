import datetime
import time
from typing import Any, Dict

from core.globals import site
from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.admin.site import APIDocsApp
from fastapi_amis_admin.amis import TabsModeEnum
from fastapi_amis_admin.amis.components import InputImage, Page, PageSchema
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.enums import IntegerChoices
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from starlette.requests import Request
from starlette.templating import Jinja2Templates

api_docs_app = site.get_admin_or_create(APIDocsApp)  # Get or create a default APIDocsApp instance


@api_docs_app.register_admin
class DocsAdmin(admin.IframeAdmin):
    page_schema = PageSchema(label="Docs", icon="fa fa-book")
    src = "/docs"


@api_docs_app.register_admin
class ReDocsAdmin(admin.IframeAdmin):
    # Set page menu information
    page_schema = PageSchema(label="Redocs", icon="fa fa-book")

    # Set redirect link
    @property
    def src(self):
        return f"{self.app.site.settings.site_url}/redoc"


@site.register_admin
class GitHubLinkAdmin(admin.LinkAdmin):
    # Set page menu information via page_schema class attribute
    page_schema = PageSchema(label="GitHub", icon="fa fa-github")
    # Set redirect link
    link = "https://github.com/amisadmin/fastapi_amis_admin"


@site.register_admin
class AmisPageApp(admin.AdminApp):
    page_schema = PageSchema(label="AmisPage", icon="fa fa-link", tabsMode=TabsModeEnum.radio)

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(
            HelloWorldPageAdmin,
            CurrentTimePageAdmin,
            UserRegFormAdmin,
        )


class HelloWorldPageAdmin(admin.PageAdmin):
    page_schema = PageSchema(label="HelloWorld", icon="fa fa-link")
    page = Page(title="Title", body="Hello World!")


class CurrentTimePageAdmin(admin.PageAdmin):
    page_schema = PageSchema(label="CurrentTime", icon="fa fa-link")

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        page.body = "The current time is: " + time.strftime("%Y-%m-%d %H:%M:%S")
        return page


class UserGender(IntegerChoices):
    unknown = 0, "Secret"
    man = 1, "Male"
    woman = 2, "Female"


class UserRegFormAdmin(admin.FormAdmin):
    page_schema = PageSchema(label="UserRegForm", icon="fa fa-link")

    class schema(BaseModel):
        username: str = Field(..., title="Username")
        password: str = Field(..., title="Password", amis_form_item="input-password")
        birthday: datetime.datetime = Field(None, title="Birth Date")
        gender: UserGender = Field(UserGender.unknown, title="Gender")
        is_active: bool = Field(True, title="Active")
        avatar: str = Field(
            None,
            title="Avatar",
            max_length=100,
            amis_form_item=InputImage(maxLength=1, maxSize=2 * 1024 * 1024, receiver="post:/admin/file/upload"),
        )

    async def handle(self, request: Request, data: schema, **kwargs) -> BaseApiOut:
        if data.username == "amisadmin" and data.password == "amisadmin":
            return BaseApiOut(msg="Registration successful!", data={"token": "xxxxxx"})
        return BaseApiOut(status=-1, msg="Username or password incorrect!")


@site.register_admin
class TemplatePageApp(admin.AdminApp):
    page_schema = PageSchema(label="TemplatePage", icon="fa fa-link", tabsMode=TabsModeEnum.chrome)

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(
            SimpleTemplateAdmin,
            ElementTemplateAdmin,
        )


class DemoJinja2Admin(admin.TemplateAdmin):
    templates: Jinja2Templates = Jinja2Templates(directory="apps/demo/templates")


class SimpleTemplateAdmin(DemoJinja2Admin):
    page_schema = PageSchema(label="Jinja2", icon="fa fa-link")
    template_name = "simple.html"

    async def get_page(self, request: Request) -> Dict[str, Any]:
        return {"current_time": datetime.datetime.now()}


class ElementTemplateAdmin(DemoJinja2Admin):
    page_schema = PageSchema(label="ElementUI", icon="fa fa-link")
    template_name = "element.html"


@site.register_admin
class FastAPIUserAuthAdmin(admin.LinkAdmin):
    page_schema = PageSchema(label="FastAPIUserAuth", icon="fa fa-angellist")
    link = "http://user-auth.demo.amis.work/"


@site.register_admin
class AmisEditorAdmin(admin.IframeAdmin):
    page_schema = PageSchema(label="AmisEditorDemo", icon="fa fa-edit", sort=-100)
    src = "https://aisuda.github.io/amis-editor-demo/"
