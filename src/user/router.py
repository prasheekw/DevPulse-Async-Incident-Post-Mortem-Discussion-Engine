from fastapi import APIRouter, Depends, status, Request
from .dtos import UserCreate, UserResponse, LoginSchema
from src.utils.database import get_db
from src.user import controller
from sqlalchemy.orm import Session
from .model import User

router = APIRouter()

@router.put("/update_user/{user_id}", response_model=UserResponse)
def update_one_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db), user:User = Depends(controller.is_authenticated)):
    return controller.update_user(user_id, db, user,user_update)

@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_user(user_id: int, db:Session = Depends(get_db), user:User = Depends(controller.is_authenticated)):
    return controller.delete_user(user_id, db, user)

@router.post("/register", response_model=UserResponse ,status_code=201)
def register(body:UserCreate, db:Session = Depends(get_db)):
    return controller.register(body, db)

@router.post("/login", status_code=200)
def login(body:LoginSchema, db: Session = Depends(get_db)):
    return controller.login(body, db)

@router.get("/is_auth", status_code=200)
def is_authenticated(request:Request, db:Session = Depends(get_db), response_model=UserResponse):
    return controller.is_authenticated(request, db)
