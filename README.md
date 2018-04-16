# logs-analysis-project
Udacity Full Stack Nano Degree Databases Project

This project uses a news database provided by UDACITY.

To run this program:

  1-Pyhton must be installed
  2-newsdata.sql must be downloaded and extracted followint the steps:
    *https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91

    *TLDR: psql -d news -f newsdata.sql
  
  3- Run program via 
    * python logger.py

logger.py has three methods called in order:

1-) get_most_popular_articles => Returns most popular three articles

2-) get_most_popular_authors => Returns most popular three authors

3-) get_error_days => Returns days where errors exceeds %1 of total requests

I've created some extra views within this database:

 article_hits_view:


 CREATE VIEW article_hits_view AS
 SELECT log.path,
    log.ip,
    log.method,
    log.status,
    log."time",
    log.id
   FROM log
  WHERE log.path <> '/'::text AND log.status = '200 OK'::text;

 article_popularity:


 CREATE VIEW article_popularity AS
 SELECT article_hits_view.path,
    count(*) AS cnt
   FROM article_hits_view
  GROUP BY article_hits_view.path
  ORDER BY (count(*)) DESC;

  log_types_count: -- Shows daily grouped log types with counts and ratio of 404 responses to 200 responses. --


 CREATE VIEW log_types_count AS 
 SELECT log.status,
    log."time"::timestamp without time zone::date AS "time",
    lag(count(*)) OVER (PARTITION BY (log."time"::timestamp without time zone::date)) AS lag,
    count(*) AS cnt,
    to_char(count(*)::numeric * 100.00 / lag(count(*)) OVER (PARTITION BY (log."time"::timestamp without time zone::date))::numeric, '9.999'::text) AS pct
   FROM log
  GROUP BY log.status, (log."time"::timestamp without time zone::date)
  ORDER BY (log."time"::timestamp without time zone::date);


