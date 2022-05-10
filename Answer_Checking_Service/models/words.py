from pydantic import BaseModel
from datetime import datetime

class Word(BaseModel):
  word: str
  timestamp: datetime

