from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from jose import JWTError,jwt
from datetime import datetime,timedelta
from .database import get_db
from . import models
from .config import settings

ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXP_MINUTES = settings.access_token_exp_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    to_encode.update({'exp':datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXP_MINUTES)})
    return jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='invalid credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )
    user_id = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

