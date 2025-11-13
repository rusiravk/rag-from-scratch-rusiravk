from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ToDo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

todos = {
    0:ToDo(id=0, title="Sample Task", description="This is a sample task", completed=False),
    1:ToDo(id=1, title="Another Task", description="This is another task", completed=True)
}

@app.get("/")
def index() -> dict[str, dict[int, ToDo]]:
    return {'todos': todos}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int) -> ToDo:
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail=f"ToDo {todo_id} not found")
    return todos[todo_id]

@app.post("/todos/", status_code=201)
def create_todo(todo: ToDo) -> ToDo:
    if todo.id in todos:
        raise HTTPException(status_code=400, detail=f"ToDo {todo.id} already exists")
    todos[todo.id] = todo
    return todo