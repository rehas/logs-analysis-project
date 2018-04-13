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

#test_connect()

# Returns most popular articles filtered by only successful HTTP responses

def get_most_popular_articles():
    db = psycopg2.connect(DBPATH)
    c = db.cursor()

# Creating query string parameter
# Joining tables based on string replacement
# Matching slug line with path
# 
# article_popularity is a view based on log table
# Filters out the unsuccessful http attempts
# Groups by path and adds a column named cnt for hit count to each path
    
    qry_get_most_popular_articles = \
     "select title, cnt \
        from articles join article_popularity \
        on articles.slug = replace(path, '/article/', '');"
    c.execute(qry_get_most_popular_articles)
    res = c.fetchall()

# Iterator is used to print only the first three most popular articles
# This functionality can be embedded into the psql query but I thought
# maybe in the future this function might be based on parameters. 

    iterator = 0
    for i in res:
        if iterator < 3:
            print("Article Name: %s Total Succesful Views: %s" %( i[0],  i[1]))
        iterator +=1
    db.close()
    return res

get_most_popular_articles()