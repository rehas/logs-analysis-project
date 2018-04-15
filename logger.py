#!/usr/bin/env python3

import psycopg2

DBPATH = "dbname=news"


# Returns most popular articles filtered by only successful HTTP responses
def get_most_popular_articles():
    db = psycopg2.connect(DBPATH)
    c = db.cursor()
    # Creating query string parameter
    # Joining tables based on string replacement
    # Matching slug line with path
    # ----------------------------------
    # article_popularity is a view based on log table
    # Filters out the unsuccessful http attempts
    # Groups by path and adds a column named cnt for hit count to each path
    # ----------------------------------
    qry_get_most_popular_articles = \
        "select title, cnt \
        from articles join article_popularity \
        on articles.slug = replace(path, '/article/', '');"
    c.execute(qry_get_most_popular_articles)
    res = c.fetchall()
    print("\n PRINTING MOST POPULAR ARTICLES \n")
    # ----------------------------------
    # Iterator is used to print only the first three most popular articles
    # This functionality can be embedded into the psql query but I thought
    # maybe in the future this function might be based on parameters.
    # # ----------------------------------
    iterator = 0
    for i in res:
        if iterator < 3:
            print("Article Name: %s Total Succesful Views: %s" % (i[0],  i[1]))
        iterator += 1
    db.close()
    return res

get_most_popular_articles()
# Returns most popular authors filtered by only successful HTTP responses


def get_most_popular_authors():
    db = psycopg2.connect(DBPATH)
    c = db.cursor()
    # Adding author id and author name column to the
    # # previous most popular articles query article_popularity view
    # ----------------------------------
    qry_get_most_popular_authors = \
        "select author, name, sum(cnt) \
         from articles, authors, article_popularity \
         where articles.slug = replace(path, '/article/', '') \
         and authors.id = articles.author \
         group by author, name order by sum desc"
    c.execute(qry_get_most_popular_authors)
    res = c.fetchall()
    print("\n PRINTING MOST POPULAR AUTHORS \n")
    # Iterator is used to print only the first three most popular articles
    # This functionality can be embedded into the psql query but I thought
    # maybe in the future this function might be based on parameters.
    # # ----------------------------------
    iterator = 0
    for i in res:
        if iterator < 3:
            print("Author Name: %s Total Succesful Views: %s" % (i[1],  i[2]))
        iterator += 1
    db.close()
    return res

get_most_popular_authors()
# Returns days where errors exceed more than %1 of total requests


def get_error_days():
    # Get all logs, based on date and type.
    # log_types_count is a view showing logs grouped by type and day
    # it also includes other status type counts within the row
    # including percentage
    # ----------------------------------
    db = psycopg2.connect(DBPATH)
    c = db.cursor()
    qry_get_error_days = \
        "select time, lag + cnt as total, cnt as errors, \
        to_char(cnt::float / (cnt + lag), '9.99') as P \
        from log_types_count \
        where (cnt::float / (cnt + lag) > 0.01::float) \
        "
    c.execute(qry_get_error_days)
    res = c.fetchall()
    print("\n PRINTING MOST ERROR DAYS \n")
    iterator = 0
    for i in res:
        if iterator < 3:
            print("Date: %s -- Total Hits: %s -- Errors: %s -- Percentage: %s"
                  % (i[0],  i[1], i[2], i[3]))
        iterator += 1
    print("\n END OF ANALYSIS \n")
    db.close()
    return res

get_error_days()
