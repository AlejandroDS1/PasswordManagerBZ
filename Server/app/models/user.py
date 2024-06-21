from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class UserBase(SQLModel):
    email: str | None = Field(unique=True)
    name: str | None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=True)
    hashed_password : bytes | None = Field(nullable=False)
    salt : bytes | None = Field(nullable=False)

    def toDict(self):
        return {"name" : self.name, "email" : self.email}    

class ErrorCode_DATA(Enum):
    WRONG_EMAIL: str = "Email user is not valid"
    ALREADY_EMAIL: str = "Email already in use"
    UNEXPECTED_ERROR : str = "An unexpected error oucrred, try again later or contact with support"


# CRUD methods, this might be moved to another module later
from sqlmodel import Session, select
from app.encryption.encryptionManager import create_password
from re import search

def create_user(session : Session, user_ : dict) -> User | ErrorCode_DATA:
    try:
        if not check_email(user_["email"]): return ErrorCode_DATA.WRONG_EMAIL

        # Check if user with this email is already in database
        if session.exec(select(User).where(User.email == user_["email"])).one_or_none(): return ErrorCode_DATA.ALREADY_EMAIL

        # Create user
        hashed_user_password, salt = create_password(user_["password"])
        userin : User = User(email=user_["email"], name=user_["username"], hashed_password=hashed_user_password, salt=salt) # Encrpyt user password

        user : User = User.model_validate(userin)

        session.add(user)
        session.commit()

        user = session.exec(select(User).where(User.email == user_["email"])).one()
    except: return ErrorCode_DATA.UNEXPECTED_ERROR
    return user


def check_email(email : str) -> bool:
    # Check if email is a real email
    return search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)

