#! /usr/bin/env python3
# "Database code" for article view report generation

import datetime
import psycopg2

DBNAME = "news"

# Queries 3 most popular articles from log table
title1 = "=====Section 1: Most Popular Three Articles of All Time="
query1 = """
select title, count(*) as num
from log join articles
on articles.slug = substring(log.path from '/article/(.*)')
group by title order by num desc limit 3
"""

# Queries 3 most popular articles from log table
title2 = "=====Section 2: Most Popular Authors of All Time========="
query2 = """
select name, sum(num) as total_view
from authors join
(
  select author, count(*) as num
  from log join articles
  on articles.slug = substring(log.path from '/article/(.*)')
  group by author
) as article_view
on authors.id = article_view.author
group by name order by total_view desc """

title3 = "=====Section 3: Days When Error Rate > 1.0% ============="
query3 = """
select day, fail_rate from (select date_trunc('day', time) as day,
  cast(sum(case when status != '200 OK' then 1 else 0 end) as float)
  /cast(count(*) as float) as fail_rate
from log group by day) as fetch_fr where fail_rate > 0.01
"""

def generate_report(cursor, query, title, format_str, factor):
    cursor.execute(query)
    rows = cursor.fetchall()

    print ""
    print title
    for row in rows:
      print format_str.format(row[0], factor * row[1])


def main():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    generate_report(c, query1, title1, """ "{}" --- {}""", 1)
    generate_report(c, query2, title2, """{} --- {} views""", 1)
    generate_report(c, query3, title3,
        """{0:%B %d, %Y} --- {1:.2f}% error""", 100.0)

    db.close()

if __name__ == '__main__':
    main()
