from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils

router = APIRouter(prefix='/users')

@router.get('/',response_model=List[schemas.UserOut])
def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post('/')
def create_user(new_user:schemas.UserIn,db:Session=Depends(get_db)):
    user = models.User(username=new_user.username,password=utils.create_password_hash(new_user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message':'new user added successfully'}