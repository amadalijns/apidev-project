from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

import secrets
import crud
import models
import schemas
from database import SessionLocal, engine
import os

app = FastAPI()
security = HTTPBasic()

# Creëer de database tabellen
models.Base.metadata.create_all(bind=engine)


# Functie om de database sessie op te halen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint om een nieuwe taak te maken
@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):

    # Authenticatie toevoegen
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"zwaardvis"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Controleren of taak al bestaat op basis van de naam
    db_task = crud.get_task_by_name(db, name=task.name)
    if db_task:
        raise HTTPException(status_code=400, detail="Een taak met deze naam bestaat al!")
    return crud.create_task(db, task)


# Endpoint om alle taken op te halen
@app.get("/tasks", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)


# Endpoint om een specifieke taak op te halen op basis van ID
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Taak {task_id} is niet gevonden!")
    return task


# Endpoint om de status van een taak bij te werken
@app.put("/tasks/{task_id}")
def update_task_status(task_id: int, completed: bool, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):

    # Authenticatie toevoegen
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"zwaardvis"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    db_task = crud.update_task_status(db, task_id, completed)
    if db_task is None:
        raise HTTPException(status_code=404, detail=f"Taak {task_id} is niet gevonden!")
    return db_task


# Endpoint om een taak te verwijderen op basis van ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):

    # Authenticatie toevoegen
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"zwaardvis"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return crud.delete_task_by_id(db, task_id=task_id)


# Endpoint om alle taken te verwijderen
@app.delete("/tasks")
def delete_tasks(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):

    # Authenticatie toevoegen
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"zwaardvis"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return crud.delete_all_tasks(db)
