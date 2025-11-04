from sqlalchemy import Column,String,Integer,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    
    user = relationship('User',back_populates='posts')
    owner_id = Column(Integer,ForeignKey('users.id'))
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    
    posts = relationship('Post',back_populates='user')
    
class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer,ForeignKey('users.id'),primary_key=True)
    post_id = Column(Integer,ForeignKey('posts.id'),primary_key=True)