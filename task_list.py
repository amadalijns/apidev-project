from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    name: str
    completed: bool


tasks = [
    Task(id=1, name="Taak1", completed=False),
    Task(id=2, name="Taak2", completed=True),
    Task(id=3, name="Taak3", completed=False)
]  # Lijst met taken


@app.get("/tasks", response_model=list[Task])
async def read_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return None
