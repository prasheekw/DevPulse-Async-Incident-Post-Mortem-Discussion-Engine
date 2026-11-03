from fastapi import FastAPI
from src.utils.database import Base, engine
from src.user.router import router as user_router
from src.posts.router import router as posts_router
from src.comments.router import router as comment_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(posts_router)
app.include_router(comment_router)