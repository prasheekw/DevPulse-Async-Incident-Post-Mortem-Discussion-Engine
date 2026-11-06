from fastapi import HTTPException, status
from src.comments.dtos import CommentSchema, commentResponse
from src.comments.model import comments
from sqlalchemy.orm import Session
from src.user.model import User
from src.posts.model import Posts


def create_comment(comment:CommentSchema, user:User, db:Session):
    post = db.get(Posts, comment.post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    comment_data = comment.model_dump()
    if comment.parent_comment_id is not None:
        parent = db.get(comments, comment.parent_comment_id)

        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")
        
        if parent.is_deleted:
            raise HTTPException(status_code=400,detail="Cannot reply to a deleted comment")

        if parent.post_id != comment.post_id:
            raise HTTPException(
                status_code=400,
                detail="Parent comment does not belong to this post"
            )

    new_comment=comments(
        comment = comment_data["comment"],
        post_id=comment.post_id,
        user_id=user.id,
        parent_comment_id=comment.parent_comment_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

def get_comments_by_post_id(post_id:int, db:Session):
    post = db.get(Posts, post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    all_comments = db.query(comments).filter(comments.post_id == post_id).order_by(comments.id).all()

    comment_map = {
        c.id: {
            "id": c.id,
            "comment": c.comment,
            "parent_comment_id": c.parent_comment_id,
            "is_deleted": c.is_deleted,
            "replies": []
        }
        for c in all_comments
    }
    
    root_comments = []

    for c in all_comments:

        current_comment = comment_map[c.id]

        if c.parent_comment_id is None:
            root_comments.append(current_comment)

        else:
            parent = comment_map.get(c.parent_comment_id)

            if parent is not None:
                parent["replies"].append(current_comment)

    return root_comments

def update_comment(comment_id:int, user:User, body:CommentSchema, db:Session):
    db_comment = db.get(comments, comment_id)

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="you're not allowed to perform this action")
    
    if db_comment.is_deleted:
        raise HTTPException(status_code=400,detail="Cannot edit a deleted comment")
    
    db_comment.comment = body.comment

    db.commit()
    db.refresh(db_comment)

    return db_comment

def delete_comment(comment_id:int, user:User, db:Session):
    db_comment = db.get(comments, comment_id)

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="you're not allowed to perform this action")
    
    if db_comment.is_deleted:
        raise HTTPException(status_code=404,detail="Comment already deleted")
    
    db_comment.is_deleted = True
    db_comment.comment = "[This comment has been deleted]"
    db.commit()
    db.refresh(db_comment)

    return status.HTTP_204_NO_CONTENT
