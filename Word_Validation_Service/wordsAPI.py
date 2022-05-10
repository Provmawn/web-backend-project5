from http import HTTPStatus
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import contextlib
import sqlite3
from typing import List

app = FastAPI()

WORDLE_WORD_LENGTH = 5


class Word(BaseModel):
    word: str


def get_db():
    with contextlib.closing(sqlite3.connect("WordValidationDB")) as db:
        db.row_factory = sqlite3.Row
        yield db


@app.post("/WordValidations")
def validate_word(guess: Word,  db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        """
        SELECT word FROM gameDictionary WHERE word = (?);
        """, (guess.word.lower(), )
    )
    word_found = cur.fetchall()

    return {"word_valid": True} if word_found else {"word_valid": False}


@app.post("/WordValidations/AddWord")
def add_word(new_word: Word, db: sqlite3.Connection = Depends(get_db)):
    db.execute(
        """
        INSERT INTO gameDictionary (word) VALUES (?);
        """, (new_word.word.lower(), )
    )
    db.commit()

    return HTTPStatus.OK


@app.post("/WordValidations/RemoveWord")
def delete_word(del_word: Word, db: sqlite3.Connection = Depends(get_db)):
    db.execute(
        """
        DELETE FROM gameDictionary WHERE word = (?);
        """, (del_word.word.lower(), )
    )
    db.commit()

    return HTTPStatus.OK
