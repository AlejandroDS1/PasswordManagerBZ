from sqlmodel import SQLModel, Field
from typing import Optional

class UserBase(SQLModel):
    email: str | None = Field(default=None, unique=True)
    name: str | None = Field(nullable=False)
    
    public_key: str | None = Field(nullable=False)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password : str = Field(nullable=False)

    
    def toDict(self):
        return {"id": self.id, "name" : self.name, "email" : self.email}    

class UserCreate(UserBase):
    password: str

# CRUD methods, this might be moved to another module later
from sqlmodel import Session
import re

def create_user(session : Session, user : dict) -> User:
    # Check if email is a real email
    if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user["email"]):
        return None
    
    #user : User = User(id=None, email=user["email"], name=user["username"], public_key=user["public_key"], password=user["password"]) 
    userin : UserCreate = UserCreate(email="acntero@gmail.com", name="username", public_key="loquesea", password="otracosa")

    #user : User = User.model_validate(userin)
    user : User = User.model_validate(userin)

    session.add(user)
    session.commit()

    session.refresh(user)

    return user
        
    