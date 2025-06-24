from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import declarative_base, relationship

from enum import Enum as PyEnum


Base = declarative_base()

class PostStatus(PyEnum):
    WAITING = 'waiting'
    PUBLISHED = 'published'
    DECLINED = 'declined'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String)
    file_id = Column(String)
    caption = Column(Text)
    status = Column(Enum(PostStatus), default=PostStatus.WAITING)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
