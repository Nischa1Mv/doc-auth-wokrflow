from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id:Optional[str] = Field(alias="id")
    name: str
    fb_user_id: str
    fb_access_token: str
    wba_id: str
    phone_number: str
