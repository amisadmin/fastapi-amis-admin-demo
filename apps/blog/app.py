from fastapi_amis_admin.amis_admin.admin import AdminApp

from apps.blog.admin import CategoryAdmin, ArticleAdmin, TagAdmin
from fastapi_amis_admin.amis.components import PageSchema
from fastapi_amis_admin.amis_admin import admin

from core.adminsite import site


@site.register_admin
class BlogApp(admin.AdminApp):
    page_schema = PageSchema(label='博客应用',icon='fa fa-wordpress')

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(CategoryAdmin,ArticleAdmin,TagAdmin)
 