from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
import os

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_name(db, name=task.name)  # Controleren of taak al bestaat op basis van de naam

    if db_task:
        raise HTTPException(status_code=400, detail="Task with this name already exists")

    return crud.create_task(db, task)


@app.get("/tasks", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task_by_id(db, task_id=task_id)


@app.put("/tasks/{task_id}")
def update_task_status(task_id: int, completed: bool, db: Session = Depends(get_db)):
    db_task = crud.update_task_status(db, task_id, completed)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task_by_id(db, task_id=task_id)


@app.delete("/tasks")
def delete_tasks(db: Session = Depends(get_db)):
    return crud.delete_all_tasks(db)
