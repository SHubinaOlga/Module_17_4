from fastapi import FastAPI
from app2.routers_dz import user, task
from app.backend.db import engine, Base

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)

# uvicorn app2.main_2:app
# http://127.0.0.1:8000/docs