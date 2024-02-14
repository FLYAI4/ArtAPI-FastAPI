import pydantic
from typing import Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class UserGeneratedInfo(pydantic.BaseModel):
    origin_img: Any
    text_content: Any
    coord_content: Any


class Base(DeclarativeBase):
    pass


class Content(Base):
    __tablename__ = 'user_content'

    seq = Column(Integer, primary_key=True)
    id = Column(String(500), nullable=False)
    generated_id = Column(String(500), nullable=False)