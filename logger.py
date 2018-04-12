import psycopg2

DBPATH = "dbname=news"

def test_connect():
    db = psycopg2.connect(DBPATH)
    c = db.cursor()
    qry_selectall = "select * from authors"
    c.execute(qry_selectall)
    res = c.fetchall()
    for i in res:
        print i
    db.close()
    return res

test_connect()