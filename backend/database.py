from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine, select, or_

postgres_name = "beatmap_similarity"
postgres_url = f"postgresql://postgres:@localhost:5432/{postgres_name}"
engine = create_engine(postgres_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
