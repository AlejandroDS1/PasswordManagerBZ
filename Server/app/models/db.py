from pydantic_core import MultiHostUrl
from sqlalchemy import create_engine
from sqlmodel import Session
from typing import Annotated
from collections.abc import Generator

DB_NAME="../../../PsswdMG.db"

engine = create_engine(
            str(MultiHostUrl.build(
                scheme="sqlite",
                host='',
                path=DB_NAME,
            ))
        )

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as en:
        yield en

db : Session = Annotated[Session(engine), get_db]