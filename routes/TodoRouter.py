from typing import Annotated, List
from fastapi import APIRouter, HTTPException, status, Depends, Path

from utils.database import get_db, DB_DEPENDENCY
from schemas.TodoSchema import TodoCreate, TodoResponse
from controllers import TodoController as todo_controller

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TodoResponse])
async def get_all_todos(db: DB_DEPENDENCY):
    return todo_controller.get_all(db)

@router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def get_todo(
    db: DB_DEPENDENCY, 
    todo_id: int = Path(..., gt=0)
):
    todo = todo_controller.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
async def create_todo(db: DB_DEPENDENCY, todo_request: TodoCreate):
    try:
        return todo_controller.create(db, todo_request)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def update_todo(
    db: DB_DEPENDENCY, 
    todo_request: TodoCreate, 
    todo_id: int = Path(..., gt=0)
):
    existing_todo = todo_controller.get_by_id(db, todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    try:
        return todo_controller.update(db, existing_todo, todo_request)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: DB_DEPENDENCY, 
    todo_id: int = Path(..., gt=0)
) -> None:
    existing_todo = todo_controller.get_by_id(db, todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    try:
        todo_controller.delete(db, existing_todo)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))