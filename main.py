# main.py
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Static files for CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# In-memory database
class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool

todo_list = []

@app.get("/", response_class=HTMLResponse)
def read_todos(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todo_list": todo_list})

@app.post("/add")
def add_todo(title: str = Form(...)):
    todo_id = len(todo_list) + 1
    todo_list.append(TodoItem(id=todo_id, title=title, completed=False))
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle/{todo_id}")
def toggle_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            todo.completed = not todo.completed
            break
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{todo_id}")
def delete_todo(todo_id: int):
    global todo_list
    todo_list = [todo for todo in todo_list if todo.id != todo_id]
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
