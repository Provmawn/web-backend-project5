from pydantic import BaseModel
from datetime import datetime


class Game(BaseModel):
    user_id: str
    game_id: int
    finished: datetime
    guesses: int
    won: bool


class User(BaseModel):
    user_id: str
    username: str