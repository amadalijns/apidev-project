from sqlalchemy.orm import Session

import models
import schemas


def get_taks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task_by_id(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()

