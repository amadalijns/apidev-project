from sqlalchemy.orm import Session

import models
import schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.Task):
    db_task = models.Task(name=task.name, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task_by_id(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": f"Task with id {task_id} has been deleted"}
    return {"message": f"Task with id {task_id} not found"}
