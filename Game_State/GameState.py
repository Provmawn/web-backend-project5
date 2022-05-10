from types import SimpleNamespace

class GameState:
    max_guesses = 6
    def __init__(self, user_id, game_id, prev_game_ids = [], guesses = []):
        self.user_id = user_id
        self.game_id = game_id
        self.prev_game_ids = prev_game_ids
        self.guesses = guesses
    
    def eligible_guess(self):
        return len(self.guesses) < self.max_guesses
    
    def guesses_remaining(self):
        return self.max_guesses - len(self.guesses)
    
    def add_guess(self, guess: str):
        self.guesses.append(guess)
    
    def json_to_GameState(json_obj: SimpleNamespace):
        return GameState(json_obj.user_id, json_obj.game_id, json_obj.prev_game_ids, json_obj.guesses)