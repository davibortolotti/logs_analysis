#!/usr/bin/python3
import psycopg2


# What are the most popular three articles of all time?
def mostpopart():
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(
        """SELECT title, count(title) AS views
        FROM most_popular
        GROUP BY title
        ORDER BY views DESC
        LIMIT 3;"""
    )
    return cursor.fetchall()
    db.close()


# Who are the most popular article authors of all time?
def mostpopauth():
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(
        """SELECT name, views
        FROM authors
        JOIN most_popular_auth ON authors.id = most_popular_auth.author
        ORDER BY views DESC;"""
    )
    return cursor.fetchall()
    db.close()


#  On which days did more than 1% of requests lead to errors?
def daysoferror():
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(
        """SELECT hits.day, cast((cast("hits not found"as float)*100/cast(hits
        as float)) as numeric(2,1)) as percentage
        FROM hits join notfound on hits.day = notfound.day
        WHERE "hits not found"*100/hits > 1;"""
    )
    return cursor.fetchall()
    db.close()


most_popular_articles = mostpopart()
most_popular_authors = mostpopauth()
days_of_error = daysoferror()

# RESULTS:
print("The three most popular articles of all time are: \n")

for pair in most_popular_articles:
    print("%s - %s views" % (pair[0], pair[1]))
print("\nThe most popular authors, in order, are: \n")

for pair in most_popular_authors:
    print("%s - %s views" % (pair[0], pair[1]))
print("\nThe days that more than 1% of the requests lead to errors are:")

for pair in days_of_error:
    print(pair[0].strftime("%b %d, %Y") + " - %s%% errors" % (pair[1]))
