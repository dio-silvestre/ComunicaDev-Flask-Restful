from sqlalchemy.orm import relationship
from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import (
    Integer,
    String,
    Text
)

from app.services.helper import BaseModel


@dataclass
class CategoryModel(db.Model, BaseModel):

    id: int
    type: str
    description: str
   
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    lessons = relationship('LessonModel', cascade='all, delete-orphan')
