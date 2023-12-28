from sqlalchemy.orm import Session
from fastapi import logger
import models, schemas
from loguru import logger

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    db_todos = db.query(models.Todo).offset(skip).limit(limit).all()
    return db_todos


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(content=todo.content, due_date=todo.due_date)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, done: bool):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db_todo.done = done
        db.commit()
        db.refresh(db_todo)
        return db_todo
    else:
        logger.warning(f"No such todo with id: {todo_id}")

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        logger.info(f"Deleted todo with id: {todo_id}")
    else:
        logger.warning(f"No such todo with id: {todo_id}")
