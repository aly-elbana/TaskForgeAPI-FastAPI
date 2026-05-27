from sqlalchemy.orm import Session
from models.TodoModel import Todo
from schemas.TodoSchema import TodoCreate

def get_all(db: Session):
    return db.query(Todo).all()

def get_by_id(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create(db: Session, todo_data: TodoCreate):
    new_todo = Todo(**todo_data.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def update(db: Session, existing_todo: Todo, update_data: TodoCreate):
    data = update_data.model_dump()
    for key, value in data.items():
        setattr(existing_todo, key, value)
    db.commit()
    db.refresh(existing_todo)
    return existing_todo

def delete(db: Session, existing_todo: Todo):
    db.delete(existing_todo)
    db.commit()