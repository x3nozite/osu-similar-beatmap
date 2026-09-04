import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, create_engine, select, or_

load_dotenv()

postgres_url = os.getenv("DATABASE_URL")
engine = create_engine(str(postgres_url))


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
