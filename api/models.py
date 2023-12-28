import datetime
from sqlalchemy import Column, String, Integer, Boolean
from database import Base


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    done = Column(Boolean, default=False)
    due_date = Column(String)