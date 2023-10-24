import datetime
from typing import Any, List

from core.globals import site
from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.admin import AdminAction, AdminApp
from fastapi_amis_admin.amis.components import (
    ActionType,
    Dialog,
    PageSchema,
    TableColumn,
)
from fastapi_amis_admin.amis.constants import LevelEnum
from fastapi_amis_admin.crud.parser import LabelField
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.enums import IntegerChoices
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from sqlmodel.sql.expression import Select
from starlette.requests import Request

from apps.blog.models import Article, Category, Tag


@site.register_admin
class BlogApp(admin.AdminApp):
    page_schema = PageSchema(label="Blog Application", icon="fa fa-wordpress")

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(
            CategoryAdmin,
            ArticleAdmin,
            TagAdmin,
        )


class CategoryAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="Category Management", icon="fa fa-folder")
    model = Category
    search_fields = [Category.name]


class TagAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="Tag Management", icon="fa fa-tags")
    model = Tag
    search_fields = [Tag.name]
    link_model_fields = [Tag.articles]


class UserGender(IntegerChoices):
    unknown = 0, "Unknown"
    man = 1, "Male"
    woman = 2, "Female"


class TestAction(admin.ModelAction):
    action = ActionType.Dialog(tooltip="Custom Form Action",icon="fa fa-star",level=LevelEnum.warning, dialog=Dialog())

    class schema(BaseModel):
        username: str = Field(..., title="Username")
        password: str = Field(..., title="Password", amis_form_item="input-password")
        birthday: datetime.datetime = Field(None, title="Birth Date")
        gender: UserGender = Field(UserGender.unknown, title="Gender")
        is_active: bool = Field(True, title="Is Active")

    async def handle(self, request: Request, item_id: List[str], data: schema, **kwargs) -> BaseApiOut[Any]:
        items = await self.admin.fetch_items(*item_id)
        return BaseApiOut(data={"item_id": item_id, "data": data, "items": list(items)})


class ArticleAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="Article Management", icon="fa fa-file")
    model = Article
    list_display = [
        Article.id,
        Article.title,
        Article.img,
        Article.status,
        Category.name,
        TableColumn(type="tpl", label="Custom Template Column", tpl='<a href="${source}" target="_blank">ID:${id},Title:${title}</a>'),
        Article.create_time,
        Article.description,
        Category.name.label("category"),
        LabelField(
            Category.name.label("category2"),
            Field("Default Category", title="Category Name"),
        ),
    ]
    search_fields = [Article.title, Category.name]
    link_model_fields = [Article.tags]
    admin_action_maker = [
        lambda self: TestAction(self, name="test_action", label="Custom Action", flags=["item", "bulk"]),
        lambda self: AdminAction(
            self,
            name="iframe_action",
            flags=["item"],
            action=ActionType.Dialog(
                icon="fa fa-star",
                level=LevelEnum.warning,
                tooltip="Custom Iframe Action",
                dialog=Dialog(
                    size="lg",
                    body=amis.Iframe(
                        src=f"{self.site.router_path}/TemplatePageApp/page/element.html",
                        height=500,
                        events={
                            "detail": {
                                "actionType": "dialog",
                                "dialog": {"title": "Dialog", "body": "iframe passed to amis id is：${iframeId}"},
                            }
                        },
                    ),
                ),
                size="md",
            ),
        ),
        lambda self: AdminAction(
            self,
            name="toolbar_action1",
            flags=["toolbar"],
            action=ActionType.Ajax(
                label="Toolbar Ajax Action",
                level=LevelEnum.danger,
                api="https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm",
            ),
        ),
        lambda self: AdminAction(
            self,
            name="toolbar_action2",
            flags=["toolbar"],
            action=ActionType.Link(
                label="Toolbar Link Action", level=LevelEnum.secondary, link="https://github.com/amisadmin/fastapi_amis_admin"
            ),
        ),
        lambda self: AdminAction(
            self,
            name="toolbar_action3",
            flags=["toolbar"],
            action=ActionType.Drawer(
                label="Toolbar Drawer Action",
                level=LevelEnum.info,
                drawer={
                    "title": "Form Settings",
                    "body": {
                        "type": "form",
                        "api": "https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm?waitSeconds"
                        "=1",
                        "body": [
                            {"type": "input-text", "name": "text", "label": "Text"},
                            {
                                "type": "input-number",
                                "name": "number",
                                "label": "Number",
                                "placeholder": "",
                                "inline": True,
                                "value": 5,
                                "min": 1,
                                "max": 10,
                            },
                            {"type": "input-rating", "count": 5, "value": 3, "label": "Rating", "name": "rating"},
                            {"type": "input-datetime", "name": "datetime", "inline": True, "label": "Date + Time"},
                        ],
                    },
                },
            ),
        ),
    ]
    display_item_action_as_column = True

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(Category)
