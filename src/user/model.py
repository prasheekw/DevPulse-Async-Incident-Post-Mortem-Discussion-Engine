from src.utils.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email:Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password:Mapped[str] = mapped_column(String, nullable=False)