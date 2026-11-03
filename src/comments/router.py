from fastapi import APIRouter, Depends, status
from typing import List
from src.comments.model import comments
from src.comments import controller
from src.comments.dtos import CommentSchema, commentResponse
from src.utils.database import get_db
from sqlalchemy.orm import Session
from src.user.model import User
from src.posts.model import Posts
from src.user.controller import is_authenticated

router = APIRouter(prefix="/comments")

@router.post("/create_comment", response_model=commentResponse)
def post_create(comment:CommentSchema , user:User = Depends(is_authenticated),db:Session= Depends(get_db)):
    return controller.create_comment(comment,user,db)

@router.get("/get_comments_by_post_id/{post_id}",response_model=List[commentResponse])
def get_comments_by_post_id(post_id:int, db:Session= Depends(get_db)):
    return controller.get_comments_by_post_id(post_id,db)

@router.put("/update_comment/{comment_id}", response_model= commentResponse)
def update_comment(comment_id:int, body:CommentSchema ,user:User = Depends(is_authenticated), db:Session = Depends(get_db)):
    return controller.update_comment(comment_id,user,body,db)

@router.delete("/delete_comment/{comment_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id:int, user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    controller.delete_comment(comment_id,user,db)
    return None