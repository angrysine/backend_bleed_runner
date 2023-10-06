from sqlalchemy import Column, Integer, String, Float

from config.rds import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    user_secret = Column(String)
    