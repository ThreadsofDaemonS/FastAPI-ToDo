from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db, engine
from models import Todo, Base
from schemas import TodoItem

app = FastAPI()

# Static files for CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

async def init_db():
    """Asynchronous database initialization"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/", response_class=HTMLResponse)
async def read_todos(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).order_by(Todo.id))
    todo_list = result.scalars().all()
    return templates.TemplateResponse("index.html", {"request": request, "todo_list": todo_list})

@app.post("/add")
async def add_todo(title: str = Form(...), db: AsyncSession = Depends(get_db)):
    new_todo = Todo(title=title, completed=False)
    db.add(new_todo)
    await db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle/{todo_id}")
async def toggle_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalars().first()
    if todo:
        todo.completed = not todo.completed
        await db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.delete("/delete/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalars().first()
    if todo:
        await db.delete(todo)
        await db.commit()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
