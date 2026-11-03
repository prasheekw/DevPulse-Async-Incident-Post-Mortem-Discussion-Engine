from fastapi import APIRouter, Depends, status
from typing import List
from src.posts import controller
from src.posts.dtos import PostSchema, PostResponseSchema, PostUpdateSchema
from src.utils.database import get_db
from sqlalchemy.orm import Session
from src.user.model import User
from src.user.controller import is_authenticated

router = APIRouter(prefix="/posts")

@router.post("/create_post", response_model=PostResponseSchema)
def post_create(post:PostSchema , user:User = Depends(is_authenticated),db:Session= Depends(get_db)):
    return controller.create_post(post,user,db)

@router.get("/all_posts",response_model=List[PostResponseSchema])
def get_all_posts(user:User = Depends(is_authenticated), db:Session= Depends(get_db)):
    return controller.get_all_post(user,db)

@router.get("/post/{post_id}")
def get_postby_id(post_id:int, user:User=Depends(is_authenticated), db:Session=Depends(get_db)):
    return controller.get_postby_id(post_id,db)

@router.put("/update_post/{post_id}", response_model= PostResponseSchema)
def update_post(post_id:int, body:PostUpdateSchema ,user:User = Depends(is_authenticated), db:Session = Depends(get_db)):
    return controller.update_post(post_id,user,body,db)

@router.delete("/delete_post/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int, user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return controller.delete_post(post_id,user,db)