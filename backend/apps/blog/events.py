from sqlalchemy import event
from sqlalchemy.future import Connection

from apps.blog.models import Article


@event.listens_for(Article, "before_insert")
def receive_before_insert(mapper, connection: Connection, article: Article):
    """监听创建文章"""
    # sess = object_session(article)
    # do something


@event.listens_for(Article.status, "set")
def receive_set(article: Article, value, old, initiator):
    """监听文章状态改变"""
    # sess = object_session(article)
    # do something
