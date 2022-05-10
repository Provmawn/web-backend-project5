from . import decorators

from datetime import datetime
from datetime import timedelta
import sqlite3
import json

def read_json_from_file(path: str):
    with open(path) as fd:
        return json.load(fd)

@decorators.singleton
class WordsDB:
    def __init__(self):
        print('Loading Word Database')
        self.connection = sqlite3.connect('database/words.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

        # load words from the file
        words = read_json_from_file('static/answers.json')

        # create a (word, date) record for every word
        timestamp = datetime.now()
        now = datetime(timestamp.year, timestamp.month, timestamp.day)
        words = [(word, now + timedelta(days=i)) for i, word in enumerate(words)]

        # populate table
        self.cursor.execute('''DROP TABLE IF EXISTS words''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS words (word TEXT,
                                                                 date TIMESTAMP)''')
        self.cursor.executemany('INSERT INTO words (word, date) VALUES (?, ?)', words)
        self.connection.commit()

    def __repr__(self):
        records = self.cursor.execute('''SELECT rowid, * FROM words''').fetchall()
        records = [str(record) for record in records]
        return '\n'.join(records) + '\n'

    def __del__(self):
        self.connection.close()
    
    def select_by_word(self, word: str):
        return self.cursor.execute('''SELECT rowid, * FROM words WHERE word = ?''', (word,)).fetchall()

    def select_by_timestamp(self, timestamp: datetime):
        return self.cursor.execute('''SELECT rowid, * FROM words WHERE date = ?''', (timestamp,)).fetchall()

    def update_by_timestamp(self, word: str, timestamp: datetime):
        self.cursor.execute('''UPDATE words SET word = ? WHERE date = ?''', (word, timestamp))
