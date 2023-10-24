from sqlalchemy import event
from sqlalchemy.future import Connection

from apps.blog.models import Article


@event.listens_for(Article, "before_insert")
def receive_before_insert(mapper, connection: Connection, article: Article):
    """Listen for the creation of an article"""
    # sess = object_session(article)
    # do something


@event.listens_for(Article.status, "set")
def receive_set(article: Article, value, old, initiator):
    """Listen for changes to the article's status"""
    # sess = object_session(article)
    # do something


