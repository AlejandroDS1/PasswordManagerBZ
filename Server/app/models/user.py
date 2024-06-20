from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class UserBase(SQLModel):
    email: str | None = Field(default=None, unique=True, primary_key=True)
    name: str | None
    
    public_key: str | None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=True)
    password : str | None

    def toDict(self):
        return {"id": self.id, "name" : self.name, "email" : self.email}    

class UserCreate(UserBase):
    password: str


class ErrorCode_DATA(Enum):
    WRONG_EMAIL: str = "Email user is not valid"
    ALREADY_EMAIL: str = "Email already in use"


# CRUD methods, this might be moved to another module later
from sqlmodel import Session, select
from re import search

def create_user(session : Session, user_ : dict) -> User | ErrorCode_DATA:
    
    if not check_email(user_["email"]): return ErrorCode_DATA.WRONG_EMAIL

    # Check if user with this email is already in database
    if session.exec(select(User).where(User.email == user_["email"])).one_or_none(): return ErrorCode_DATA.ALREADY_EMAIL

    # Create user
    userin : UserCreate = UserCreate(email=user_["email"], name=user_["username"], public_key=user_["public_key"], password=user_["password"]) 

    user : User = User.model_validate(userin)

    # session.add(user)
    # session.flush()
    # session.commit()

    # user = session.exec(select(User).where(User.email == user_["email"])).one()
    return user


def check_email(email : str) -> bool:
    # Check if email is a real email
    return search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)

