from fastapi import FastAPI, Depends, status
from Stats_Service.models import User, Game
from Stats_Service.update.update import redisClient
import sqlite3
import uuid
import contextlib
from http import HTTPStatus
import httpx
import json
from datetime import datetime
from pydantic import BaseModel

class Word(BaseModel):
    word: str

app = FastAPI()

@app.post("/game/new")
def start_new_game(username: str):
    # get the user_id using the username
    r = httpx.get("http://localhost:9999/api/v2/user/" + username)
    user_id_content = json.loads(r.content.decode('utf-8'))

    # get all of the games played using the user_id 
    r = httpx.get("http://localhost:9999/api/v2/user/" + user_id_content["user_id"] + "/gamesPlayed")
    games_content = json.loads(r.content.decode('utf-8'))

    # get the max game_id + 1 as new game_id
    game_ids = []
    for game in games_content:
        game_ids.append(game['game_id'])
    new_game_id = max(game_ids) + 1
    new_game = {"user_id": user_id_content["user_id"], "game_id": new_game_id}
    print(new_game)

    # create a new game using the create new game endpoint
    r = httpx.post("http://localhost:9999/api/v4/create", data=json.dumps(new_game))

    response = {
        "status": "new",
        "user_id": user_id_content["user_id"],
        "game_id": new_game_id
    }

    return response

class Guess(BaseModel):
    word: str
    user_id: str

@app.post("/game/{game_id}")
def guess_a_word(game_id: int, guess: Guess):

    user_id = guess.user_id
    word = guess.word

    # get game state
    r = httpx.get("http://localhost:9999/api/v4/restore/" + user_id)
    game_state_content = json.loads(r.content.decode('utf-8'))
    game_state = json.loads(game_state_content[user_id])

    # setup response
    status = "valid" 
    remaining_guesses = len(game_state["guesses"])
    letters = {}

    # check if word is valid
    r = httpx.post("http://localhost:9999/api/v1/WordValidations", data=json.dumps({"word": word}))
    valid_word_content = json.loads(r.content.decode('utf-8'))
    if not valid_word_content["word_valid"]:
        return {"status": "invalid", "remaining": remaining_guesses}

    # record guess and update game state
    r = httpx.put("http://localhost:9999/api/v4/update/" + user_id + "/" + word, data=json.dumps({"user_id": user_id, "guess": word}))
    game_state_content = json.loads(r.content.decode('utf-8'))
    game_state = json.loads(game_state_content[user_id])

    # perform guess
    now = datetime.now().timestamp()
    r = httpx.post("http://localhost:9999/api/v3/check", data=json.dumps({"word": word, "timestamp": str(now)}))
    letter_colors_content = json.loads(r.content.decode('utf-8'))
    
    # check if guess is correct

    for color in letter_colors_content:
        guess_status = "win"
        if color == "yellow":
            guess_status = "incorrect"
        status = guess_status

    response = {
        "status": status,
        "remaining": remaining_guesses,
        "letters": letter_colors_content,
    }

    return response
    
