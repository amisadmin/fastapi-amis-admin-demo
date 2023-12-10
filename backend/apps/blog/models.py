from datetime import datetime
from typing import List, Optional

from fastapi_amis_admin.amis.components import ColumnImage, InputImage, InputRichText
from fastapi_amis_admin.models import IntegerChoices, Field,SQLModel,ChoiceType
from sqlalchemy import Column, String
from sqlmodel import Relationship


class ArticleStatus(IntegerChoices):
    unpublished = 0, "未发布"
    published = 1, "已发布"
    inspection = 2, "审核中"
    disabled = 3, "已禁用"


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title="CategoryName", sa_column=Column(String(100), unique=True, index=True, nullable=False))
    description: str = Field(default="", title="Description", amis_form_item="textarea")
    status: bool = Field(False, title="status")
    articles: List["Article"] = Relationship(back_populates="category")


class ArticleTagLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(..., title="TagName", sa_column=Column(String(255), unique=True, index=True, nullable=False))
    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTagLink)


class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title="ArticleTitle", max_length=200)
    img: str = Field(
        "",
        title="ArticleImage",
        max_length=300,
        amis_form_item=InputImage(maxLength=1, maxSize=2 * 1024 * 1024, receiver="post:/admin/file/upload"),
        amis_table_column=ColumnImage(width=100, height=60, enlargeAble=True),
    )
    description: str = Field(default="", title="ArticleDescription", amis_form_item="textarea")
    status: ArticleStatus = Field(ArticleStatus.unpublished, title="status",sa_type=ChoiceType(ArticleStatus))
    content: str = Field(..., title="ArticleContent", amis_form_item=InputRichText())
    create_time: Optional[datetime] = Field(default_factory=datetime.utcnow, title="CreateTime")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", title="CategoryId")
    source: str = Field(default="", title="ArticleSource", max_length=200)

    category: Optional[Category] = Relationship(back_populates="articles")

    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTagLink)
