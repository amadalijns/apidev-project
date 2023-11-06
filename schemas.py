from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str | None = None
    completed: bool


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
