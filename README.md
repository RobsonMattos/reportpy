# Report

This project, developed in python 3, aims to present an informative summary of the type of article that the visitors of the site like, answering:
- What articles are the most popular and accessed ;
- Who are the authors of the most popular articles of all time;
- On which days more than 1% of the requests generated errors.

# Prerequisites:
This reporting tool is a Python program that uses the `psycopg2` module to connect to the database.
To execute:
    - you'll need to have python3 installed
    - Install psycopg2
        - $ pip install psycopg2
    Create views on the postgres database (news)

The views to use it with the solution are presented below:

------------------------------------------------------------------------------

-- drop view vw_author_articles;

CREATE VIEW vw_author_articles as
select a.name as author, b.title, c.qtd
from 
  authors  a,
  articles b,
  vw_log_articles c
WHERE
  a.id = b.author
  and b.title = c.title;

------------------------------------------------------------------------------

-- drop view vw_log_articles;

CREATE VIEW vw_log_articles
AS
  select count(a.path) as qtd, b.title
  from
    log a,
    articles b
  where 
  status like '200%'
    and b.slug = substring(a.path from 10 for char_length (a.path))
  group by b.title
  order by 1 desc;

----------------------------------------------------------------------------

-- drop view vw_author;
create view vw_author
as
    select author, sum(qtd) as qtd
    from
        vw_author_articles
    group by author
    order by 2 desc;

----------------------------------------------------------------------------

-- drop view vw_quiz_one;

create view vw_quiz_one
as
    select title || ' - ' || qtd || ' views' as result
    from
        vw_log_articles
limit 3;

----------------------------------------------------------------------------

-- drop view vw_quiz_two;

create view vw_quiz_two
as
  select author || ' - ' || qtd || ' views'
  from
    vw_author;

----------------------------------------------------------------------------

-- drop view vw_quiz_three;

create view vw_quiz_three as
select
  a.date || ' - ' || 
  round((cast(b.qtd as numeric) * 100) / cast(a.qtd as numeric), 2) || '% errors'
from
  (SELECT count(time) as qtd, to_char(time, 'Month DD, YYYY') as date
  FROM
    log
  group by date
  order by date) a,
  (SELECT count(time) as qtd, to_char(time, 'Month DD, YYYY') as date
  FROM
    log
  WHERE
      status like '404%'
  group by date
  order by date) b
WHERE
  a.date = b.date 
  and (cast(b.qtd as numeric) * 100) / cast(a.qtd as numeric) > 1;

--------------------------------------------------------------------


To run the tool, type at the command prompt
$ python report.py

# Authors and contributions:
This project was developed by Robson Mattos rjnmattos@gmail.com