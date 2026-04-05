from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI()
start_time = time.time()
tasks = []

REQUEST_COUNT = Counter("app_requests_total", "Total app requests")

@app.get("/", response_class=HTMLResponse)
def home():
    REQUEST_COUNT.inc()
    return """
    <html>
        <head>
            <title>Cloud-Native Task Manager</title>
        </head>
        <body>
            <h1>Cloud-Native Task Manager</h1>
            <p>App is running successfully.</p>
            <p>Use /health to check health</p>
            <p>Use /tasks to see tasks</p>
            <p>Use /metrics for monitoring</p>
        </body>
    </html>
    """

@app.get("/health")
def health():
    REQUEST_COUNT.inc()
    return {"status": "healthy"}

@app.get("/uptime")
def uptime():
    REQUEST_COUNT.inc()
    return {"uptime_seconds": round(time.time() - start_time, 2)}

@app.get("/tasks")
def get_tasks():
    REQUEST_COUNT.inc()
    return {"tasks": tasks}

@app.post("/tasks/{task_name}")
def add_task(task_name: str):
    REQUEST_COUNT.inc()
    tasks.append(task_name)
    return {"message": "Task added", "tasks": tasks}

@app.delete("/tasks/{task_name}")
def delete_task(task_name: str):
    REQUEST_COUNT.inc()
    if task_name in tasks:
        tasks.remove(task_name)
        return {"message": "Task deleted", "tasks": tasks}
    return {"message": "Task not found", "tasks": tasks}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)