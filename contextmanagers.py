import sqlite3
from contextlib import contextmanager

@contextmanager
def SQL(query):
    conn = sqlite3.connect("site.db", check_same_thread=False)
    db = conn.cursor()
    db.execute(query)
    rows = db.fetchall()
    yield rows
    conn.commit()
    conn.close()

""" 
# TEST
with SQL("SELECT * from user") as rows:
    for row in rows:
        print(row[1])
"""