from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from src.user.model import User
from src.utils.config import settings
from src.utils.database import get_db
from datetime import datetime
from jwt.exceptions import InvalidTokenError
import jwt

def is_authenticated(request:Request, db:Session = Depends(get_db)):
    try:
        jwt_token = request.headers.get("authorization")
        if not jwt_token:
            raise HTTPException(status_code=401, detail="you are Unauthorized")
        token = jwt_token.split(" ")[-1]

        data = jwt.decode(jwt_token, settings.SECRET_KEY, settings.ALGORITHM)

        user_id = data.get("_id")
        exp_time = data.get("exp")

        current_time = datetime.now().timestamp()

        if exp_time is None:
            raise HTTPException(status_code=401, detail="Token expiration is missing")

        if current_time > exp_time:
            raise HTTPException(status_code=401, detail="you are Unauthorized")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="you are unauthorized")
        
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="You are unauthorized")

    return user