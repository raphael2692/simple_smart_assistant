from pydantic import BaseModel

class TodoBase(BaseModel):
    content: str
    due_date: str
    important: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    done: bool = False
    
    class config:
        orm_mode = True