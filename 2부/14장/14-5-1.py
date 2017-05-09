class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "Point(%f, %f)" % (self.x, self.y)

import sqlite3
def PointAdapter(point):
    return "%f:%f" % (point.x, point.y)

def PointConverter(s):
    x, y = list(map(float, s.decode().split(":")))
    return Point(x, y)

sqlite3.register_adapter(Point, PointAdapter)
sqlite3.register_converter("point", PointConverter)

p = Point(4, -3.2)
p2 = Point(-1.4, 6.2)

con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
cur.execute("create table test(p point)")
cur.execute("insert into test values (?)", (p, ))
cur.execute("insert into test(p) values (?)", (p2,))

cur.execute("select p from test")
print([r[0] for r in cur])
cur.close()
con.close()
