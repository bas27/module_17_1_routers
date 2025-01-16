from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete  # Функции работы с записями.
from slugify import slugify  # Функция создания slug-строки

router = APIRouter(prefix='/task', tags=['task'])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/")
async def all_tasks(db: DbSession):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get("/task_id")
async def task_by_id(task_id: int, db: DbSession):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        return task
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.post("/create")
async def create_task(task: CreateTask, db: DbSession, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        db.execute(insert(Task).values(title=task.title,
                                       content=task.content,
                                       priority=task.priority,
                                       user_id=user_id,
                                       slug=slugify(task.title)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")


@router.put("/update")
async def update_task(db: DbSession, update_task: UpdateTask, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        db.execute(update(Task).where(Task.id == task_id).values(title=update_task.title,
                                                                 content=update_task.content,
                                                                 priority=update_task.priority))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")


@router.delete("/delete")
async def delete_task(db: DbSession, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
