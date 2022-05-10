import json
import sqlite3

print("Initializing valid words database...")
file = open('/usr/share/dict/words', 'r')
poss_words = file.readlines()
file.close()
words = []
for word in poss_words:
    stripped = word.strip()
    if stripped.isalpha() and len(stripped) == 5:
        words.append((stripped.lower(), ))

db = sqlite3.connect("WordValidationDB")
cursor = db.cursor()
cursor.execute(
    '''DROP TABLE IF EXISTS gameDictionary;''')
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS gameDictionary ( id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT);''')

query = '''INSERT INTO gameDictionary (word) VALUES (?);'''
cursor.executemany(query, words)
db.commit()
print(cursor.rowcount)
db.close()