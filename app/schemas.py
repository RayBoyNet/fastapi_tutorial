from pydantic import BaseModel,conint
from datetime import datetime

class UserIn(BaseModel):
    username: str
    password: str
    
class UserOut(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime
    
class PostIn(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    user: UserOut
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0,le=1)
    
class VotePostOut(BaseModel):
    Post: PostOut
    votes: int