from pydantic import BaseModel, Field, field_validator

class PostSchema(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str = Field(min_length=1, max_length=5000)

    @field_validator("title", "content")
    @classmethod
    def validate_whitespace(cls, value: str):
        if not value.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return value

class PostResponseSchema(BaseModel):
    id: int
    title: str
    content: str

class PostUpdateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str = Field(min_length=1, max_length=5000)
