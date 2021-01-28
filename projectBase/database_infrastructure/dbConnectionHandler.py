import psycopg2


def createConnectionToDatabase():
    """
    docstring
    """
    connection = psycopg2.connect(user="postgres",
                                  password="poc123",
                                  host="localhost",
                                  port=5555,
                                  database="redditdb")
    return connection
