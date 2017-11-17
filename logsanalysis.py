#!/usr/bin/python3
import psycopg2

# function for fetching data in the database
def return_query_data(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


# What are the most popular three articles of all time?
most_popular_articles = return_query_data(
    """SELECT title, count(title) AS views
    FROM most_popular
    GROUP BY title
    ORDER BY views DESC
    LIMIT 3;"""
)

most_popular_authors = return_query_data(
    """SELECT name, views
    FROM authors
    JOIN most_popular_auth ON authors.id = most_popular_auth.author
    ORDER BY views DESC;"""
)

#  On which days did more than 1% of requests lead to errors?
days_of_error = return_query_data(
    """SELECT hits.day, cast((cast("hits not found"as float)*100/cast(hits
    as float)) as numeric(2,1)) as percentage
    FROM hits join notfound on hits.day = notfound.day
    WHERE "hits not found"*100/hits > 1;"""
)

# RESULTS:
print("The three most popular articles of all time are: \n")
for title, views in most_popular_articles:
    print("{} - {} views".format(title, views))

print("\nThe most popular authors, in order, are: \n")
for author, views in most_popular_authors:
    print("{} - {} views".format(author, views))

print("\nThe days that more than 1% of the requests lead to errors are:")
for date, percentage in days_of_error:
    print(date.strftime("%b %d, %Y") + " - {}% errors".format(percentage))
