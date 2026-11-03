from src.utils.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING ##These imports are used by type checkers but aren't executed at runtime, so they avoid the circular import.

if TYPE_CHECKING:
    from src.comments.model import comments

class Posts(Base):
    __tablename__ = "posts"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(150), nullable=False)
    content:Mapped[str] = mapped_column(String(5000), nullable=False)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id", ondelete="CASCADE"))
    comments: Mapped[list["comments"]] = relationship(back_populates="post")