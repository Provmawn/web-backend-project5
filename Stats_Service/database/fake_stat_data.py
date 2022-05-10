#!/usr/bin/env python3

import contextlib
import datetime
import random
import sqlite3
import uuid
from db_constants import total_databases, stat_db_name, db_file_extension

import faker


NUM_STATS = 1_000
NUM_USERS = 100
YEAR = 2022

random.seed(YEAR)
fake = faker.Faker()
faker.Faker.seed(YEAR)
cur_user_ids = []
user_shard = [[] for _ in range(total_databases)]
game_shard = [[] for _ in range(total_databases)]

print("Beginning to insert fake stat data...")
for _ in range(NUM_USERS):
    username = str(fake.simple_profile()['username'])
    user_id = str(uuid.uuid4())
    shard_key = int(uuid.UUID(user_id)) % (total_databases)
    user_shard[shard_key].append((user_id, username))

jan_1 = datetime.date(YEAR, 1, 1)
today = datetime.date.today()
num_days = (today - jan_1).days
for _ in range(NUM_STATS):
    rand_shard_key = random.randint(0, total_databases - 1)
    user_id, _username = user_shard[rand_shard_key][random.randint(0, len(user_shard[rand_shard_key]) - 1)]
    game_id = random.randint(1, num_days)
    finished = jan_1 + \
        datetime.timedelta(random.randint(0, num_days))
    # N.B. real game scores aren't uniformly distributed...
    guesses = random.randint(1, 6)
    # ... and people mostly play to win
    won = random.choice([False, True, True, True])
    game_shard[rand_shard_key].append((user_id, game_id, finished, guesses, won))


for db_num in range(total_databases):
    cur_db = stat_db_name + str(db_num) + db_file_extension
    with contextlib.closing(sqlite3.connect(cur_db)) as db:
        for i in range(len(user_shard[db_num])):
            try:
                user_id, username = user_shard[db_num][i]
                cur_user_ids.append(user_id)
                db.execute('INSERT INTO users(user_id, username) VALUES(?, ?)', [
                           user_id, username])

            except sqlite3.IntegrityError:
                cur_user_ids.remove(user_id)
                continue
        db.commit()
        print("Finished Users table")
        jan_1 = datetime.date(YEAR, 1, 1)
        today = datetime.date.today()
        num_days = (today - jan_1).days
        for i in range(len(game_shard[db_num])):
            try:
                user_id, game_id, finished, guesses, won = game_shard[db_num][i]
                if user_id not in cur_user_ids:
                    continue
                
                db.execute(
                    """
                    INSERT INTO games(user_id, game_id, finished, guesses, won)
                    VALUES(?, ?, ?, ?, ?)
                    """,
                    [user_id, game_id, finished, guesses, won]
                )
            except sqlite3.IntegrityError:
                continue
        db.commit()
        print("Finished Games table")
        cur_user_ids.clear()
