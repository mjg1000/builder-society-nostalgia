from typing import List
from sqlmodel import Session, select
from songModel import Song
from songDatabase import engine

def daoGetAllSongs() -> List[Song]:
    with Session(engine) as session:
        statement = select(Song)
        songs = session.exec(statement).all()
        return songs