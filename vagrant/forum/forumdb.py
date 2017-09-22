# "Database code" for the DB Forum.

import bleach
import datetime
import psycopg2 

DBNAME = "forum"
def get_posts():
  db = psycopg2.connect(database = DBNAME)
  c = db.cursor()
  query = "select content, time from posts"
  c.execute(query)
  rows = c.fetchall()
  db.close()

  return rows 

def add_post(content):
  db = psycopg2.connect(database = DBNAME)
  c = db.cursor()
  bleachedContent = bleach.clean(content)
  c.execute("insert into posts values (%s)", (bleachedContent,))
  db.commit()
  db.close()


