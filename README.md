# logs-analysis-project
Udacity Full Stack Nano Degree Databases Project

This project uses a news database provided by UDACITY.

I've created some extra views within this database:

 article_hits_view:

 SELECT log.path,
    log.ip,
    log.method,
    log.status,
    log."time",
    log.id
   FROM log
  WHERE log.path <> '/'::text AND log.status = '200 OK'::text;

 article_popularity:

 SELECT article_hits_view.path,
    count(*) AS cnt
   FROM article_hits_view
  GROUP BY article_hits_view.path
  ORDER BY (count(*)) DESC;

  log_types_count -- Shows daily grouped log types with counts and ratio of 404 responses to 200 responses. --

  SELECT log.status,
    log."time"::timestamp without time zone::date AS "time",
    lag(count(*)) OVER (PARTITION BY (log."time"::timestamp without time zone::date)) AS lag,
    count(*) AS cnt,
    to_char(count(*)::numeric * 1.00 / lag(count(*)) OVER (PARTITION BY (log."time"::timestamp without time zone::date))::numeric, '9.999'::text) AS pct
   FROM log
  GROUP BY log.status, (log."time"::timestamp without time zone::date)
  ORDER BY (log."time"::timestamp without time zone::date);



logger.py has three functions called in order:

1-) get_most_popular_articles => Returns most popular three articles

2-) get_most_popular_authors => Returns most popular three authors

3-) get_error_days => Returns days where errors exceeds %1 of total requests