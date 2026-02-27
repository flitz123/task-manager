from fastapi import FastAPI, Request
from app.api import auth, tasks
from app.db.base import Base
from app.db.session import engine
from app.models.role import Role
from app.db.session import SessionLocal
import time

Base.metadata.create_all(bind=engine)

db = SessionLocal()
if not db.query(Role).first():
    db.add(Role(name="admin"))
    db.add(Role(name="user"))
    db.commit()
db.close()

app = FastAPI(title="Enterprise Task Manager API")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url} - {duration}")
    return response

app.include_router(auth.router)
app.include_router(tasks.router)
