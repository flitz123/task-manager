from fastapi import FastAPI, Request
from app.api import auth, tasks
from app.db.base import Base
from app.db.session import engine
from app.models.role import Role
from app.db.session import SessionLocal
import time
