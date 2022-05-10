import sqlite3
import redis

redisClient = redis.StrictRedis(host="localhost", port=6379, db=0)

db = sqlite3.connect("StatDB_0.db")
db1 = sqlite3.connect("StatDB_1.db")
db2 = sqlite3.connect("StatDB_2.db")

def updateTop10Wins(db: sqlite3.Connection = db, db1: sqlite3.Connection = db1, 
                       db2: sqlite3.Connection = db2):
    win_agg = []
    cur = db.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        win_agg.append(win)
    wins.clear()

    cur = db1.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        win_agg.append(win)
    wins.clear()

    cur = db2.execute(
        """
        SELECT * FROM wins LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        win_agg.append(win)
    wins.clear()

    def sort_wins(row):
        return row[1]
    
    win_agg.sort(reverse=True ,key=sort_wins)
    
    return win_agg[0:10]

def updateTop10Streaks(db: sqlite3.Connection = db,
            db1: sqlite3.Connection = db1, db2: sqlite3.Connection = db2):
    streak_agg = []

    cur = db.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        streak_agg.append(win)
    wins.clear()

    cur = db1.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        streak_agg.append(win)
    wins.clear()

    cur = db2.execute(
        """
        SELECT * FROM streaks LIMIT 10;
        """
    )
    wins = cur.fetchall()
    for win in wins:
        streak_agg.append(win)
    wins.clear()

    def sort_streak(row):
        return row[1]
    
    streak_agg.sort(reverse=True, key=sort_streak)
    
    return streak_agg[0:10]

def main():
    streaks = updateTop10Streaks()
    wins = updateTop10Wins()
    
    for x in streaks:
        redisClient.zadd("Streaks", {x[0]: x[1]})
    print("Top 10 Streaks imported")
        
    for y in wins:
        redisClient.zadd("Wins", {y[0]: y[1]})
    print("Top 10 Wins imported")
 
if __name__ == "__main__":
    main()   