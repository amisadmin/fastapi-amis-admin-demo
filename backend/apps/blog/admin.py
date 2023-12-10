import datetime
from typing import Any, List, Optional

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
from fastapi_amis_admin.models import IntegerChoices, Field
from pydantic import BaseModel
from sqlmodel.sql.expression import Select
from starlette.requests import Request

from apps.blog.models import Article, Category, Tag


@site.register_admin
class BlogApp(admin.AdminApp):
    page_schema = PageSchema(label="博客应用", icon="fa fa-wordpress")

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(
            CategoryAdmin,
            ArticleAdmin,
            TagAdmin,
        )


class CategoryAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="分类管理", icon="fa fa-folder")
    model = Category
    search_fields = [Category.name]


class TagAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="标签管理", icon="fa fa-tags")
    model = Tag
    search_fields = [Tag.name]
    link_model_fields = [Tag.articles]


class UserGender(IntegerChoices):
    unknown = 0, "保密"
    man = 1, "男"
    woman = 2, "女"


class TestAction(admin.ModelAction):
    action = ActionType.Dialog(tooltip="自定义表单动作", icon="fa fa-star", level=LevelEnum.warning, dialog=Dialog())

    # 创建表单数据模型
    class schema(BaseModel):
        username: str = Field(..., title="用户名")
        password: str = Field(..., title="密码", amis_form_item="input-password")
        birthday: Optional[datetime.datetime] = Field(None, title="出生日期")
        gender: UserGender = Field(UserGender.unknown, title="性别")
        is_active: bool = Field(True, title="是否激活")

    async def handle(self, request: Request, item_id: List[str], data: schema, **kwargs) -> BaseApiOut[Any]:
        items = await self.admin.fetch_items(*item_id)
        return BaseApiOut(data={"item_id": item_id, "data": data, "items": list(items)})


class ArticleAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="文章管理", icon="fa fa-file")
    model = Article
    # 配置列表展示字段
    list_display = [
        Article.id,
        Article.title,
        Article.img,
        Article.status,
        Category.name,
        TableColumn(type="tpl", label="自定义模板列", tpl='<a href="${source}" target="_blank">ID:${id},Title:${title}</a>'),
        Article.create_time,
        Article.description,
        Category.name.label("category"),  # 重命名字段;也可以使用sqlalchemy函数, 例如:
        # func.count('*').label('article_count'), 注意在`get_select`中修改对应的sql查询语句
        LabelField(
            Category.name.label("category2"),
            Field("默认分类", title="分类名称"),  # 通过Field配置Amis表格列信息,Amis表单字段信息.
        ),
    ]
    # 配置模糊搜索字段
    search_fields = [Article.title, Category.name]
    # 配置关联模型
    link_model_fields = [Article.tags]
    # 配置自定义动作
    admin_action_maker = [
        lambda self: TestAction(self, name="test_action", label="自定义动作", flags=["item", "bulk"]),
        lambda self: AdminAction(
            self,
            name="iframe_action",
            flags=["item"],
            action=ActionType.Dialog(
                icon="fa fa-star",
                level=LevelEnum.warning,
                tooltip="自定义Iframe动作",
                dialog=Dialog(
                    size="lg",
                    body=amis.Iframe(
                        src=f"{self.site.router_path}/TemplatePageApp/page/element.html",
                        height=500,
                        events={
                            "detail": {
                                "actionType": "dialog",
                                "dialog": {"title": "弹框", "body": "iframe 传给 amis 的 id 是：${iframeId}"},
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
                label="工具条ajax动作",
                level=LevelEnum.danger,
                api="https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm",
            ),
        ),
        lambda self: AdminAction(
            self,
            name="toolbar_action2",
            flags=["toolbar"],
            action=ActionType.Link(
                label="工具条link动作", level=LevelEnum.secondary, link="https://github.com/amisadmin/fastapi_amis_admin"
            ),
        ),
        lambda self: AdminAction(
            self,
            name="toolbar_action3",
            flags=["toolbar"],
            action=ActionType.Drawer(
                label="工具条抽屉动作",
                level=LevelEnum.info,
                drawer={
                    "title": "表单设置",
                    "body": {
                        "type": "form",
                        "api": "https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm?waitSeconds"
                               "=1",
                        "body": [
                            {"type": "input-text", "name": "text", "label": "文本"},
                            {
                                "type": "input-number",
                                "name": "number",
                                "label": "数字",
                                "placeholder": "",
                                "inline": True,
                                "value": 5,
                                "min": 1,
                                "max": 10,
                            },
                            {"type": "input-rating", "count": 5, "value": 3, "label": "评分", "name": "rating"},
                            {"type": "input-datetime", "name": "datetime", "inline": True, "label": "日期+时间"},
                        ],
                    },
                },
            ),
        ),
    ]
    display_item_action_as_column = True  # 将item_action显示为列

    # 自定义查询选择器
    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(Category)
