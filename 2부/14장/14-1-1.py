import sqlite3

con = sqlite3.connect(":memory:")

with open('script.txt') as f:
    SQLScript = f.read()

cur = con.cursor()
cur.executescript(SQLScript)