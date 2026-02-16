from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# User Schemas
class UserSignup(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Class Schemas
class ClassCreate(BaseModel):
    name: str = Field(..., min_length=1)
    dateTime: datetime
    instructor: str = Field(..., min_length=1)
    availableSlots: int = Field(..., ge=1)

class ClassResponse(BaseModel):
    id: int
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingCreate(BaseModel):
    class_id: int
    client_name: str = Field(..., min_length=1)
    client_email: EmailStr

class BookingResponse(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: str
    booked_at: datetime
    fitness_class: ClassResponse
    
    class Config:
        from_attributes = True
