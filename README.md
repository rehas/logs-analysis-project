# logs-analysis-project
---
## Udacity Full Stack Nano Degree Databases Project

This project uses a news database provided by UDACITY.

Project uses psycopg2 to query a fictive news website database.

### Requirements
---
- [Vagrant] (https://www.vagrantup.com/)
- [VirtualBox] (https://www.virtualbox.org/wiki/Downloads)

Alternatively if you don't want a virtual machine environment:

- [Python3] (https://www.python.org/download/releases/3.0/)
- [psycopg2] (http://initd.org/psycopg/)
- [postgreSQL] (https://www.postgresql.org/)

### Installation
---
  
  After getting done with #Requirements

  1) [newsdata.sql] (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) should be downloaded and put in the main folder after unzipping.
  2) Create the database named news:
     - `psql` : Launch psql console
     - `\l` : Display all databases and see if there's a DB called news
     - `DROP DATABASE news` : drop the database if it exists
     - `CREATE DATABASE news` : create the new database
     - `\q` : exit the console
  3) To load the data `cd` into the directory and use command : `psql-d news -f newsdata.sql`
   -`psql` -- PostgreSQL command line
   -`-d news` -- connect to DB named news which has set up
   -`-f newsdata.sql` -- run the SQL statements in the file newsdata.sql
  
  3) Run program via: `python logger.py`

### Functionality
---

logger.py has three methods called in order:

1) `get_most_popular_articles` => Returns most popular three articles

2) `get_most_popular_authors` => Returns most popular three authors

3) `get_error_days` => Returns days where errors exceed %1 of total requests


I've created some extra views within this database:

 `article_hits_view`:

```
 CREATE VIEW article_hits_view AS
 SELECT log.path,
    log.ip,
    log.method,
    log.status,
    log."time",
    log.id
   FROM log
  WHERE log.path <> '/'::text AND log.status = '200 OK'::text;
```

` article_popularity`:

```
 CREATE VIEW article_popularity AS
 SELECT article_hits_view.path,
    count(*) AS cnt
   FROM article_hits_view
  GROUP BY article_hits_view.path
  ORDER BY (count(*)) DESC;
```
  `log_types_count`: -- Shows daily grouped log types with counts and ratio of 404 responses to 200 responses. --

```
 CREATE VIEW log_types_count AS 
 SELECT log.status,
    log."time"::timestamp without time zone::date AS "time",
    lag(count(*)) OVER (PARTITION BY (log."time"::timestamp without time zone::date)) AS lag,
    count(*) AS cnt,
    to_char(count(*)::numeric * 100.00 / lag(count(*)) OVER (PARTITION BY (log."time"::timestamp without time zone::date))::numeric, '9.999'::text) AS pct
   FROM log
  GROUP BY log.status, (log."time"::timestamp without time zone::date)
  ORDER BY (log."time"::timestamp without time zone::date);
```

### Author
- **Berat Reha Sonmez**
