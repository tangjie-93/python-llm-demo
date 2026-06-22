from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Task API")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    description: str = ""


class Task(TaskCreate):
    id: str
    done: bool = False


TASKS: dict[str, Task] = {}


def require_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != "dev-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )


@app.post("/tasks", response_model=Task, dependencies=[Depends(require_api_key)])
def create_task(payload: TaskCreate) -> Task:
    task = Task(id=str(uuid4()), **payload.model_dump())
    TASKS[task.id] = task
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(done: bool | None = None) -> list[Task]:
    tasks = list(TASKS.values())
    if done is not None:
        return [task for task in tasks if task.done is done]
    return tasks


@app.patch("/tasks/{task_id}", response_model=Task, dependencies=[Depends(require_api_key)])
def mark_done(task_id: str, done: bool = True) -> Task:
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = task.model_copy(update={"done": done})
    TASKS[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=204, dependencies=[Depends(require_api_key)])
def delete_task(task_id: str) -> None:
    if TASKS.pop(task_id, None) is None:
        raise HTTPException(status_code=404, detail="Task not found")

