import psycopg2


def createConnectionToDatabase():
    """
    docstring
    """
    connection = psycopg2.connect(user="postgres",
                                  password="poc123",
                                  host="reddit_db",
                                  port=5432,
                                  database="redditdb")
    return connection
