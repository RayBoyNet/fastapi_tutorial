from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models,utils,oauth2,schemas
from ..database import get_db

router = APIRouter()

@router.post('/login',response_model=schemas.Token)
def auth_user(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='invalid credentials'
        )
    if not utils.verify_password_hash(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='invalid credentials'
        )
    access_token = oauth2.create_access_token({'user_id':user.id})
    return {'access_token':access_token,'token_type':'Bearer'}
    