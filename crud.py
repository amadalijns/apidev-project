from sqlalchemy.orm import Session

import models
import schemas


# Functie om alle taken op te halen
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


# Functie om een taak op te halen op basis van ID
def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


# Functie om een taak op te halen op basis van naam
def get_task_by_name(db: Session, name: str):
    return db.query(models.Task).filter(models.Task.name == name).first()


# Functie om een nieuwe taak te maken en op te slaan in de database
def create_task(db: Session, task: schemas.Task):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# Functie om de status van een taak bij te werken op basis van ID
def update_task_status(db: Session, task_id: int, completed: bool):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
        return db_task
    return None


# Functie om een taak te verwijderen op basis van ID
def delete_task_by_id(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": f"Taak {task_id} is verwijderd!"}
    return {"message": f"Taak {task_id} niet gevonden!"}


# Functie om alle taken te verwijderen
def delete_all_tasks(db: Session):
    db.query(models.Task).delete()
    db.commit()
    return {"message": "Alle taken zijn verwijderd!"}
