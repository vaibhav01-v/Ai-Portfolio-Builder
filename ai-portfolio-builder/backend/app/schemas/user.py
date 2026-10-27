from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    is_verified: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    message: str = "Login successful"
