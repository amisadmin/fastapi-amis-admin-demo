from datetime import datetime
from typing import List, Optional

from fastapi_amis_admin.amis.components import ColumnImage, InputImage, InputRichText
from fastapi_amis_admin.models.enums import IntegerChoices
from fastapi_amis_admin.models.fields import Field
from sqlalchemy import Column, String
from sqlmodel import Relationship, SQLModel


class ArticleStatus(IntegerChoices):
    # Article status enum
    unpublished = 0, "Unpublished"
    published = 1, "Published"
    inspection = 2, "Under Review"
    disabled = 3, "Disabled"


class Category(SQLModel, table=True):
    # Article category
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title="Category Name", sa_column=Column(String(100), unique=True, index=True, nullable=False))
    description: str = Field(default="", title="Description", amis_form_item="textarea")
    status: bool = Field(None, title="Status")
    articles: List["Article"] = Relationship(back_populates="category")


class ArticleTagLink(SQLModel, table=True):
    # Link table between articles and tags
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", primary_key=True)


class Tag(SQLModel, table=True):
    # Article tags
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(..., title="Tag Name", sa_column=Column(String(255), unique=True, index=True, nullable=False))
    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTagLink)


class Article(SQLModel, table=True):
    # Article model
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title="Article Title", max_length=200)
    img: str = Field(
        None,
        title="Article Image",
        max_length=300,
        amis_form_item=InputImage(maxLength=1, maxSize=2 * 1024 * 1024, receiver="post:/admin/file/upload"),
        amis_table_column=ColumnImage(width=100, height=60, enlargeAble=True),
    )
    description: str = Field(default="", title="Article Description", amis_form_item="textarea")
    status: ArticleStatus = Field(ArticleStatus.unpublished, title="Status")
    content: str = Field(..., title="Article Content", amis_form_item=InputRichText())
    create_time: Optional[datetime] = Field(default_factory=datetime.utcnow, title="Create Time")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", title="Category ID")
    category: Optional[Category] = Relationship(back_populates="articles")
    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTagLink)
    source: str = Field(default="", title="Article Source", max_length=200)

