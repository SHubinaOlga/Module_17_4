from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app2.Backend.db_depends2 import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app2.Models import User
from app2.schemas_dz import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get('/{user_id}')
async def user_by_id(user_id: int, db = Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    return user

@router.post('/create')
async def create_user(create: CreateUser, db = Annotated[Session, Depends(get_db)]):
     db.execute(insert(User).values
                    (username=create.username,
                     firstname=create.firstname,
                     lastname=create.lastname,
                     age=create.age,
                     slug=slugify(create.username)))
     db.commit()
     return { 'status_code': status.HTTP_201_CREATED,
              'transaction': 'Successful'}

@router.put('/update')
async def update_user(user_update: UpdateUser, user_id: int, db : Annotated[Session, Depends(get_db)]):
    update_user = db.scalars(select(User).where(User.id == user_id)).first()
    if update_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    db.execute(update(User).where(User.id == user_id).values(
                                       firstname=user_update.firstname,
                                       lastname=user_update.lastname,
                                       age=user_update.age))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'}

@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    delete_user = db.scalars(select(User).where(User.id == user_id)).first()
    if delete_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found')
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful!'}


#python3 -m uvicorn user:app --reload
# uvicorn user:app --reload