from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    password: str
    email: str


class UserCreate(UserModel):
    password: str


class User(UserModel):
    id: int

    class Config:
        orm_mode = True
