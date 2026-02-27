from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskOut
from app.core.dependencies import get_db, get_current_user
from app.models.task import Task
from redis import Redis
from app.core.config import settings

router = APIRouter(prefix="/tasks", tags=["tasks"])

redis_client = Redis(host=settings.REDIS_HOST,
                     port=settings.REDIS_PORT, decode_response=True)


def send_email_background(title: str):
    print(f"Email sent for task: {title}")


router.post("/", response_model=TaskOut)


def create_task(task: TaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_task = Task(**task.dict(), owner_id=user.id)
    db.add(new_task)
    db.commit
    db.refresh(new_task)

    redis_client.delete(f"user_tasks: {user.id}")

    background_tasks.add_tasks(send_email_background, task.title)

    return new_task


@router.get("/", response_model=list[TaskOut])
def list_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cache_key = f"user_tasks: {user.id}: {skip}: {limit}"
    cached = redis_client.get(cache_key)
    if cached:
        return eval(cached)

    tasks = db.query(Task)\
        .filter(Task.owner_id == user.id)\
        .offset(skip).limit(limit).all()

    redis_client.setex(cache_key, 60, str([t.__dict__ for t in tasks]))
    return tasks
