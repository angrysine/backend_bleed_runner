from sqlalchemy import Column, Float, String, Integer, Boolean
from models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    user_secret = Column(String)
