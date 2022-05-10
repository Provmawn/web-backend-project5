from fastapi import FastAPI, status, HTTPException
from database import WordsDB
from models import Word
from datetime import datetime

app = FastAPI()

# Checking a valid guess against the answer for the current day
@app.post("/check")
def check_guess(guess: Word, status_code=status.HTTP_200_OK):
    words_db = WordsDB()
    today = datetime(guess.timestamp.year, guess.timestamp.month, guess.timestamp.day)
    word_of_day_record = words_db.select_by_timestamp(today)

    if not word_of_day_record:
        raise HTTPException(status_code=404, detail="Word not found")

    rowid, answer, date = word_of_day_record[0]
    result = []
    for guess_letter, answer_letter in zip(guess.word, answer):
        if guess_letter == answer_letter:
            result.append('green')
        elif guess_letter in answer:
            result.append('yellow')
        else:
            result.append('gray')

    return result

# Changing the answers for future games
@app.put("/change")
def change_answer(change: Word, status_code=status.HTTP_200_OK):
    words_db = WordsDB()
    ts = datetime(change.timestamp.year, change.timestamp.month, change.timestamp.day)
    current = words_db.select_by_timestamp(ts)
    
    if not current:
        raise HTTPException(status_code=404, detail="Word not found")
    
    #print(change.word.lower())
    if change.word.lower() == current or len(change.word) != 5:
        raise HTTPException(status_code=400, detail="Word not match parameters")
    else:
        words_db.update_by_timestamp(change.word.lower(), ts)
        new = words_db.select_by_timestamp(ts)
        
    return {"status": status_code, "changed_word": new}
