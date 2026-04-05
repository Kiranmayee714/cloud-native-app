from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import time

app = FastAPI()

start_time = time.time()

tasks = []

@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <html>
        <head>
            <title>Cloud-Native Task Manager</title>
        </head>
        <body>
            <h1>Cloud-Native Task Manager</h1>
            <p>App is running successfully.</p>
            <p>Use /health to check health</p>
            <p>Use /tasks to see tasks</p>
        </body>
    </html>
    """
    return html_content

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/uptime")
def uptime():
    return {"uptime_seconds": round(time.time() - start_time, 2)}

@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks}

@app.post("/tasks/{task_name}")
def add_task(task_name: str):
    tasks.append(task_name)
    return {"message": "Task added", "tasks": tasks}

@app.delete("/tasks/{task_name}")
def delete_task(task_name: str):
    if task_name in tasks:
        tasks.remove(task_name)
        return {"message": "Task deleted", "tasks": tasks}
    return {"message": "Task not found", "tasks": tasks}