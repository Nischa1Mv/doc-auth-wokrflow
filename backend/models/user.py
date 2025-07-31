from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Main user model (used internally or in full user responses)
class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    email: EmailStr
    password: str
    name: Optional[str] = None
    fb_user_id: Optional[str] = None
    fb_access_token: Optional[str] = None
    wba_id: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# Schema for user login (email + password only)
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for user registration (email + password + name)
class UserRegister(BaseModel):
    email: EmailStr
    password: str
