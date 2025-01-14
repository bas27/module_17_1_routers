from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete  # Функции работы с записями.
from slugify import slugify  # Функция создания slug-строки

router = APIRouter(prefix="/user", tags=["user"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/")
async def all_users(db: DbSession):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id")
async def user_by_id(user_id: int, db: DbSession):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/create")
async def create_user(user: CreateUser, db: DbSession):
    db.execute(insert(User).values(username=user.username,
                                   firstname=user.firstname,
                                   lastname=user.lastname,
                                   age=user.age,
                                   slug=slugify(user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")
async def update_user(db: DbSession, update_user: UpdateUser, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        db.execute(update(User).where(User.id == user_id).values(firstname=update_user.firstname,
                                                                 lastname=update_user.lastname,
                                                                 age=update_user.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")


@router.delete("/delete")
async def delete_user(db: DbSession, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
