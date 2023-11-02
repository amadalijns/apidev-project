from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Maak een SQLite-databse connectie
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# Maak ee ntabel voor taken als deze nog niet bestaat
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             content TEXT NOT NULL,
             completed INTEGER NOT NULL)''')
conn.commit()


# Definieer een model voor taken
class Task(BaseModel):
    id: int
    content: str
    completed: int


# Voeg een taak toe aan de databse
def add_task(content, completed):
    c.execute("INSERT INTO tasks (content, completed) VALUES (?, ?)", (content, completed))
    conn.commit()
    return c.lastrowid


# Haal alle taken op uit de databse
def get_tasks():
    c.execute("SELECT * FROM tasks")
    return c.fetchall()


# Haal een specifieke taak op uit de database op basis van de ID
def get_task(task_id):
    c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    return c.fetchall()


# Verwijder een taak uit de database op basis van de ID
def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()


@app.post('/tasks/', response_model=Task)
def create_task(task: Task):
    task_id = add_task(task.content, task.completed)
    return {"id": task_id, "content": task.content, "completed": task.completed}


@app.get('/tasks/', response_model=list[Task])
def read_tasks():
    return get_tasks()


@app.get('/tasks/{task_id}', response_model=Task)
def read_task(task_id: int):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task[0], "content": task[1], "completed": task[2]}


@app.delete('/tasks/{task_id}', response_model=dict)
def delete_task_endpoint(task_id: int):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(task_id)
    return {"message": "Task deleted"}
