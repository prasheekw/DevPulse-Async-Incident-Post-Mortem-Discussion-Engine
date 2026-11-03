from pydantic import BaseModel, ConfigDict, Field, field_validator

class CommentSchema(BaseModel):
    comment: str = Field(min_length=1, max_length= 2000)
    @field_validator("comment")
    @classmethod
    def validate_whitespace(cls, value: str):
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return value

    post_id: int
    parent_comment_id: int | None = None

class commentResponse(BaseModel):
    id: int
    comment: str
    parent_comment_id: int | None
    is_deleted: bool
    replies: list["commentResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)