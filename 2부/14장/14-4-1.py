class Average:
    def __init__(self):
        self.sum = 0
        self.cnt = 0

    def step(self, value):
        self.sum += value
        self.cnt += 1

    def finalize(self):
        return self.sum / self.cnt

import sqlite3
con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute("CREATE TABLE User(Name text, Age int);")
list = (('Tom', '16'),
    ('DSP', '33'),
    ('Derick', '25'))
cur.executemany("INSERT INTO User VALUES(?, ?);", list)

con.create_aggregate("avg", 1, Average)

cur.execute("SELECT avg(Age) FROM User")
print(cur.fetchone()[0])