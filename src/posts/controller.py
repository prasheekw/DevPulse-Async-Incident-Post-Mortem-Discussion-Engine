from fastapi import HTTPException, status
from src.posts.model import Posts
from src.posts.dtos import PostSchema, PostUpdateSchema
from sqlalchemy.orm import Session
from src.user.model import User

def create_post(post:PostSchema, user:User, db:Session):

    if not post.title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")
    
    if not post.content.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty")
    
    post_data = post.model_dump()

    new_post=Posts(
        title = post_data["title"],
        content = post_data["content"],
        user_id = user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

def get_all_post(user:User, db:Session):
    db_posts = db.query(Posts).all()
    return db_posts

def get_postby_id(post_id: int, db:Session):
    db_post = db.query(Posts).filter(Posts.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found!")
    return db_post

def update_post(post_id:int, user:User, body:PostUpdateSchema ,db:Session):
    post = db.get(Posts, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="you're not allowed to perform this action")

    post.title = body.title
    post.content = body.content

    db.commit()
    db.refresh(post)

    return post

def delete_post(post_id:int, user:User, db:Session):
    post = db.get(Posts, post_id)
    if not post:
            raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="you're not allowed to perform this action")
    db.delete(post)
    db.commit()

    return None
