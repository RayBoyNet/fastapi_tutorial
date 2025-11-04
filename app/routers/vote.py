from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import schemas,models,oauth2
from ..database import get_db

router = APIRouter(prefix='/vote')

@router.post('/')
def vote_post(vote:schemas.Vote,db:Session=Depends(get_db),user:Session=Depends(oauth2.get_current_user)):
    # check if posts exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post does not exist')
    # like the post
    if vote.direction == 1:
        found_vote = db.query(models.Vote).filter(models.Vote.user_id == user.id,models.Vote.post_id == vote.post_id).first()
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='user has already liked the post')
        new_vote = models.Vote(user_id=user.id,post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {'message':'vote added successfully'}
    else:
        found_vote = db.query(models.Vote).filter(models.Vote.user_id == user.id,models.Vote.post_id == vote.post_id).first()
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user has not liked the post')
        db.delete(found_vote)
        db.commit()
        return {'message':'vote removed successfully'}
    
@router.get('/')
def get_votes(db:Session=Depends(get_db)):
    votes = db.query(models.Vote).all()
    return votes



