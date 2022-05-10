validate: uvicorn --port $PORT0 Word_Validation_Service.wordsAPI:app --reload --root-path /api/v1
stats: uvicorn --port $PORT1 Stats_Service.api:app --reload --root-path /api/v2
answer: sh -c "cd ./Answer_Checking_Service/ && uvicorn --port $PORT2 api:app --reload --root-path /api/v3"
game_state: uvicorn --port $PORT3 Game_State.api:app --reload --root-path /api/v4
