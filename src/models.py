from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

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
    approved = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    