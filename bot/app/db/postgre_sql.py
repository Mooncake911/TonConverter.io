from sqlalchemy import Column, Integer, VARCHAR, TEXT
from base import BaseModel


class User(BaseModel):
    __tablename__ = 'users_data.db'
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    file = Column(TEXT, unique=True, nullable=True)
    format = Column(VARCHAR(8), unique=False, nullable=True)
