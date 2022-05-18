from fastapi import FastAPI, Depends
from Stats_Service.models import User, Game
from Stats_Service.update.update import redisClient
import sqlite3
import uuid
import contextlib
from http import HTTPStatus
import httpx
import json
from pydantic import BaseModel

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


