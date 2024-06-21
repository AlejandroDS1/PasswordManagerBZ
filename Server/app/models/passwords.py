from sqlmodel import SQLModel, Field
from typing import Optional

class PasswordBase(SQLModel):
    website : str | None = Field(default=None, nullable=True)
    title : str | None = Field(default=None, nullable=True)

class Password(PasswordBase, table=True):
    nonce : bytes | None = Field(nullable=False)
    encrypted_password : bytes | None = Field(nullable=False)
    id: Optional[int] = Field(default=None, primary_key=True, nullable=True)
    user_id : int | None = Field(default=None, foreign_key="user.id")

    def toDict(self):
        return {"title" : self.title, "website" : self.website, "password" : self.encrypted_password}
    
class PasswordCreate(PasswordBase):
    password: str
        