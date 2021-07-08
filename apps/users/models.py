from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    id: int


class CreateUserParams(BaseModel):
    username: str
    email: EmailStr
