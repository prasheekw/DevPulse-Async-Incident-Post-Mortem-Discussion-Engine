from fastapi import HTTPException, Request, Depends
from src.utils.database import get_db
from .model import User
from sqlalchemy.orm import Session
from .dtos import UserCreate, LoginSchema
from pwdlib import PasswordHash
from src.utils.config import settings
from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

password_hash = PasswordHash.recommended()

def update_user(user_id: int, db: Session, user:User, user_update: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail= "User not found")
    
    if user.id != db_user.id:
        raise HTTPException(status_code=403, detail="you're not allowed to perform this action")

    db_user.username = user_update.username
    db_user.email = user_update.email
    db_user.password = get_password_hash(user_update.password)
    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(user_id: int, db: Session, user:User):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail= "User not found")

    if user.id != db_user.id:
        raise HTTPException(status_code=403, detail="you're not allowed to perform this action")

    db.delete(db_user)
    db.commit()
    return None

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(body:UserCreate, db:Session):

    is_username = db.query(User).filter(User.username == body.username).first()

    if is_username:
        raise HTTPException(status_code=409, detail="Username Already Exists")

    is_email = db.query(User).filter(User.email == body.email).first()

    if is_email:
        raise HTTPException(status_code=409, detail="Email Alredy Exists")

    hash_password = get_password_hash(body.password)

    new_user = User(
        username = body.username,
        email = body.email,
        password = hash_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login(body:LoginSchema, db:Session):

    is_username = db.query(User).filter(User.username == body.username).first()
    if not is_username:
        raise HTTPException(status_code=401, detail="username is incorrect")

    valid_password = verify_password(body.password, is_username.password)

    if not valid_password:
        raise HTTPException(status_code=401, detail="password is incorrect")

    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode({"_id":str(is_username.id), "exp": exp_time.timestamp()},settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token

def is_authenticated(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = data.get("_id")
        exp_time = data.get("exp")

        current_time = datetime.now().timestamp()

        if exp_time is None:
            raise HTTPException(
                status_code=401,
                detail="Token expiration is missing"
            )

        if current_time > exp_time:
            raise HTTPException(
                status_code=401,
                detail="You are unauthorized"
            )

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="You are unauthorized"
            )

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="You are unauthorized")

    return user