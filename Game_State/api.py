from email.policy import HTTP
from http import HTTPStatus
from fastapi import FastAPI
from pydantic import BaseModel
from .GameState import GameState
from types import SimpleNamespace
import redis
import json

app = FastAPI()

# Setup redis db
r = redis.StrictRedis(host="localhost", port=6379, db=0)

class NewGame(BaseModel):
    user_id: str
    game_id: int

# Starting a new game. The client should supply a user ID and game ID when a game starts. If the user has already played the game, they should receive an error.


@app.post('/create')
def start_a_new_game(new_game: NewGame):
    # User account exists
    if r.exists(new_game.user_id):
        cur_gamestate: GameState = GameState.json_to_GameState(json.loads(
            r.get(new_game.user_id), object_hook=lambda d: SimpleNamespace(**d)))

        if new_game.game_id in cur_gamestate.prev_game_ids or new_game.game_id == cur_gamestate.game_id:
            return HTTPStatus.BAD_REQUEST

        cur_gamestate.prev_game_ids.append(cur_gamestate.game_id)
        cur_gamestate.game_id = new_game.game_id

        r.set(cur_gamestate.user_id, json.dumps(cur_gamestate, default=vars))

        return HTTPStatus.OK
    # New user account
    else:
        new_game_state = GameState(new_game.user_id, new_game.game_id)
        r.set(new_game_state.user_id, json.dumps(new_game_state, default=vars))

        return HTTPStatus.OK

# Updating the state of a game. When a user makes a new guess for a game, record the guess and update the number of guesses remaining. If a user tries to guess more than six times, they should receive an error.
# Note: you do not need to check whether the guess is valid, if the guess is correct, or report on the placement of the letters in the answer. This functionality was completed in Project 2.

@app.put('/update/{user_id}/{guess}')
def update_state_of_a_game(user_id: str, guess: str):
    
    # get gamestate object based on user_id
    cur_gamestate: GameState = GameState.json_to_GameState(json.loads(r.get(user_id), object_hook=lambda d: SimpleNamespace(**d)))
    if r.exists(cur_gamestate.user_id):

        # check if they don't have more guesses
        if not cur_gamestate.eligible_guess():
            return HTTPStatus.BAD_REQUEST

        # record the guess
        cur_gamestate.add_guess(guess)

        # update the number of guesses remaining
        r.set(cur_gamestate.user_id, json.dumps(cur_gamestate, default=vars))

        return {user_id: json.dumps(cur_gamestate, default=vars)}
    else:
        return HTTPStatus.BAD_REQUEST


# Restoring the state of a game. Upon request, the user should be able to retrieve an object containing the current state of a game, including the words guessed so far and the number of guesses remaining.


@app.get('/restore/{user_id}')
def restore_state_of_a_game(user_id: str):
    if r.exists(user_id):
        cur_gamestate: GameState = GameState.json_to_GameState(
            json.loads(r.get(user_id), object_hook=lambda d: SimpleNamespace(**d)))

        return {user_id: json.dumps(cur_gamestate, default=vars)}
    else:
        return HTTPStatus.UNPROCESSABLE_ENTITY
