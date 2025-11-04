from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,HTTPException,Depends,status
from ..database import get_db
from .. import models,schemas,oauth2
from sqlalchemy import func

router = APIRouter(prefix='/posts')

@router.get('/votes',response_model=List[schemas.VotePostOut])
def get_posts_votes(db:Session=Depends(get_db)):
    results = db.query(models.Post,func.count(models.Post.id).label('votes')).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).all()
    # results = db.query(models.Post).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).order_by(models.Post.id.desc()).all()
    posts_votes = list(map(lambda x:x._mapping,results))
    # return {'message':'Hello!!!'}
    return results

@router.get('/',response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get('/{id}',response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found'
        )
    return post

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_post(new_post:schemas.PostIn,db:Session=Depends(get_db),user:Session=Depends(oauth2.get_current_user)):
    post = models.Post(owner_id=user.id,title=new_post.title,content=new_post.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {'message':'new post added successfully'}

@router.put('/{id}')
def update_post(id:int,updated_post:schemas.PostIn,db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found'
        )
    post_query.update(updated_post.model_dump())
    db.commit()
    return {'message':'post successfully updated'}

@router.delete('/{id}')
def delete_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} not found'
        )
    db.delete(post)
    db.commit()
    return {'message':'post deleted successfully'}

@router.get('/votes')
def get_posts_votes(db:Session=Depends(get_db)):
    results = db.query(models.Post).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).all()
    posts = list(map(lambda x:x._mapping,results))
    return {'message':'Hello World'}
    # return posts
    



