import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos")
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Function to retrieve all Todos.
    """
    todos = crud.get_todos(db, skip, limit)
    return todos


@app.post("/todos")
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """
    Function to create a Todo. In the content there should be all the necessary info, including the due date.
    """
    db_todo = crud.create_todo(db, todo)
    return db_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, done: bool, db: Session = Depends(get_db)):
    """
    Function to mark an existing Todo as completed or not. Remember that id start from 0.
    """
    db_todo = crud.update_todo(db, todo_id, done)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Function to delete a Todo.
    """
    db_todo = crud.delete_todo(db, todo_id)
    return db_todo

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)