import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()


# Maak een SQLite-database connectie
def get_connection():
    return sqlite3.connect('todo.db')


# Maak een tabel voor taken als deze nog niet bestaat
def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 content TEXT NOT NULL,
                 completed INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


# Model voor taken
class Task(BaseModel):
    id: int
    content: str
    completed: int


# Voeg een taak toe aan de database
def add_task(content, completed):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (content, completed) VALUES (?, ?)", (content, completed))
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    return task_id


# Haal alle taken op uit de database
def get_tasks():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks


# Haal een specifieke taak op uit de database op basis van de ID
def get_task(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = c.fetchone()
    conn.close()
    return task


# Verwijder een taak uit de database op basis van de ID
def delete_task(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


@app.on_event("startup")
async def startup_event():
    create_table()


@app.post('/tasks/', response_model=Task)
def create_task(task: Task):
    task_id = add_task(task.content, task.completed)
    return {"id": task_id, "content": task.content, "completed": task.completed}


@app.get('/tasks/', response_model=List[Task])
def read_tasks():
    return get_tasks()


@app.get('/tasks/{task_id}', response_model=Task)
def read_task(task_id: int):
    task = get_task(task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    return {"id": task[0], "content": task[1], "completed": task[2]}


@app.delete('/tasks/{task_id}', response_model=dict)
def delete_task_endpoint(task_id: int):
    task = get_task(task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    delete_task(task_id)
    return {"message": "Task deleted"}
