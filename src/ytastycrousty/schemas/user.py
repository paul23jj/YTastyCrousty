from pydantic import BaseModel

class UserBase(BaseModel):
    identifiants: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: int
    role: str
    status: str

class Config:
    from_attribute= True