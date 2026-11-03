from pydantic import BaseModel, field_validator, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email : EmailStr
    password : str = Field(min_length=10, max_length=50)
    @field_validator("username", "password")
    @classmethod
    def validate_username(cls, value: str):
        if not value.strip():
            raise ValueError("Username or Password cannot contain only whitespace")
        return value

class UserResponse(BaseModel):
    id: int
    username : str
    email : str

class LoginSchema(BaseModel):
    username: str
    password: str