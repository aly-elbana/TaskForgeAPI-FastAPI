from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email: EmailStr 
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    role: str = Field(default="user", min_length=1, max_length=50)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)