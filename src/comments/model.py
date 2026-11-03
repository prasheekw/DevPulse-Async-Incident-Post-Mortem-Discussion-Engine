from src.utils.database import Base
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING ##These imports are used by type checkers but aren't executed at runtime, so they avoid the circular import.

if TYPE_CHECKING:
    from src.posts.model import Posts

class comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    parent_comment_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    post: Mapped["Posts"] = relationship(back_populates="comments")
    parent_comment: Mapped["comments | None"] = relationship("comments",remote_side="comments.id",back_populates="replies") # Who is my parent?
    replies: Mapped[list["comments"]] = relationship("comments",back_populates="parent_comment") # Who are my child?
    is_deleted: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False)