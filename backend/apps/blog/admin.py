import datetime
from typing import List, Any

from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.amis.components import PageSchema, Action, ActionType, Dialog, TableColumn
from fastapi_amis_admin.amis.constants import LevelEnum
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.enums import IntegerChoices
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from sqlmodel.sql.expression import Select
from starlette.requests import Request

from apps.blog.models import Category, Article, Tag
from core.adminsite import site


# @site.register_admin
# class BlogApp(admin.AdminApp):
#     page_schema = PageSchema(label='博客应用',icon='fa fa-wordpress')
#
#     def __init__(self, app: "AdminApp"):
#         super().__init__(app)
#         self.register_admin(CategoryAdmin,ArticleAdmin,TagAdmin)

@site.register_admin
class CategoryAdmin(admin.ModelAdmin):
    group_schema = PageSchema(label='Articles', icon='fa fa-wordpress')
    page_schema = PageSchema(label='分类管理', icon='fa fa-folder')
    model = Category
    search_fields = [Category.name]


@site.register_admin
class TagAdmin(admin.ModelAdmin):
    group_schema = 'Articles'
    page_schema = PageSchema(label='标签管理', icon='fa fa-tags')
    model = Tag
    search_fields = [Tag.name]
    link_model_fields = [Tag.articles]


class UserGender(IntegerChoices):
    unknown = 0, '保密'
    man = 1, '男'
    woman = 2, '女'


class TestAction(admin.ModelAction):
    action = ActionType.Dialog(label='自定义表单动作', dialog=Dialog())

    # 创建表单数据模型
    class schema(BaseModel):
        username: str = Field(..., title='用户名')
        password: str = Field(..., title='密码', amis_form_item='input-password')
        birthday: datetime.datetime = Field(None, title='出生日期')
        gender: UserGender = Field(UserGender.unknown, title='性别')
        is_active: bool = Field(True, title='是否激活')

    async def handle(self, request: Request, item_id: List[str], data: schema, **kwargs) -> BaseApiOut[Any]:
        items = await self.fetch_item_scalars(item_id)
        return BaseApiOut(data=dict(item_id=item_id, data=data, items=list(items)))


@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    group_schema = 'Articles'
    page_schema = PageSchema(label='文章管理', icon='fa fa-file')
    model = Article
    # 配置列表展示字段
    list_display = [Article.id, Article.title, Article.img,
                    Article.status, Category.name,
                    TableColumn(type='tpl', label='自定义模板列',
                                tpl='<a href="${source}" target="_blank">ID:${id},Title:${title}</a>'),
                    Article.create_time, Article.description,
                    ]
    # 配置模糊搜索字段
    search_fields = [Article.title, Category.name]
    # 配置关联模型
    link_model_fields = [Article.tags]

    # 自定义查询选择器
    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.test_action = None

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.join(Category, isouter=True)

    # 添加自定义批量操作动作
    async def get_actions_on_bulk(self, request: Request) -> List[Action]:
        actions = await super().get_actions_on_bulk(request)
        action = await self.test_action.get_action(request)
        action.label = '自定义批量操作动作'
        actions.append(action.copy())
        return actions

    # 添加自定义单项操作动作
    async def get_actions_on_item(self, request: Request) -> List[Action]:
        actions = await super().get_actions_on_item(request)
        action = await self.test_action.get_action(request)
        action.label = '自定义单项操作动作'
        actions.append(action.copy())
        return actions

    # 添加自定义工具条动作
    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        actions = await super().get_actions_on_header_toolbar(request)

        actions.append(ActionType.Ajax(label='工具条ajax动作', level=LevelEnum.danger,
                                       api='https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm'))

        actions.append(ActionType.Link(label='工具条link动作', level=LevelEnum.secondary,
                                       link='https://github.com/amisadmin/fastapi_amis_admin'))

        actions.append(ActionType.Drawer(label='工具条抽屉动作', level=LevelEnum.info,
                                         drawer={
                                             "title": "表单设置",
                                             "body": {
                                                 "type": "form",
                                                 "api": "https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm?waitSeconds=1",
                                                 "body": [
                                                     {
                                                         "type": "input-text",
                                                         "name": "text",
                                                         "label": "文本"
                                                     },
                                                     {
                                                         "type": "input-number",
                                                         "name": "number",
                                                         "label": "数字",
                                                         "placeholder": "",
                                                         "inline": True,
                                                         "value": 5,
                                                         "min": 1,
                                                         "max": 10
                                                     },
                                                     {
                                                         "type": "input-rating",
                                                         "count": 5,
                                                         "value": 3,
                                                         "label": "评分",
                                                         "name": "rating"
                                                     },
                                                     {
                                                         "type": "input-datetime",
                                                         "name": "datetime",
                                                         "inline": True,
                                                         "label": "日期+时间"
                                                     }
                                                 ]
                                             }}))
        return actions

    # 注册自定义路由
    def register_router(self):
        super().register_router()
        # 注册动作路由
        self.test_action = TestAction(self).register_router()
