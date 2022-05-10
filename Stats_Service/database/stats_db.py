import sqlite3
from db_constants import *

print("Initializing the stats sharded databases...")

# TODO: update to create 3 separate DBs

for i in range(total_databases):
    db = sqlite3.connect(stat_db_name + str(i) + db_file_extension)
    cursor = db.cursor()
    sql_file = open(sql_filename)
    cursor.executescript(sql_file.read()) 
    sql_file.close()
    db.commit()
    db.close()