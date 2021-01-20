import psycopg2


def addRecordToSubreddits(subredditRecord):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()

        recordid = subredditRecord['topicId']
        recordTopicTite = str(subredditRecord['topicTitle'])
        topicCommentCount = str(subredditRecord['topicCommentCount'])
        recordTopicScore = subredditRecord['topicScore']
        recordIsAdult = subredditRecord['isAdult']
        recordUpvote = subredditRecord['topicUpvoteRation']
        topicKey = subredditRecord['topicKeyword']
        create_table_query = f'''insert into subreddits (id,topictitle,topicscore,numberofcomments,isadult,upvoteratio,topickeyword) VALUES ('{recordid}','{recordTopicTite}','{recordTopicScore}','{topicCommentCount}','{recordIsAdult}','{recordUpvote}','{topicKey}')'''
        cursor.execute(create_table_query)
        connection.commit()
        print("Added the record!")

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)


def addRecordToComments(commentRecord):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()

        commentId = commentRecord['id']
        commentAuthor = str(commentRecord['commentAuthor'])
        commentLink = str(commentRecord['commentLink'])
        commentBody = str(commentRecord['commentBody'])
        commentScore = commentRecord['commentScore']
        commentDate = commentRecord['commentDate']
        create_table_query = f'''insert into comments (id,commentauthor,commentlink,commentBody,commentscore,commentdate) VALUES ('{commentId}','{commentAuthor}','{commentLink}','{commentBody}','{commentScore}','{commentDate}')'''
        cursor.execute(create_table_query)
        connection.commit()
        print("Added the record!")

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)


def addSearchRecord(search_keyword):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()
        create_table_query = f'''insert into search_requests (search_keyword) VALUES ('{search_keyword}')'''
        cursor.execute(create_table_query)
        connection.commit()
        print("Added the record!")

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)


def getHits():
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()
        create_table_query = f'''select search_keyword,count(*) as totalCount from search_requests GROUP BY search_keyword order by totalCount DESC limit 10'''
        cursor.execute(create_table_query)
        records = cursor.fetchall()
        return records

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)

def getHighestSubredditsbyTopComments(keyword):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()
        create_table_query = f'''select * from subreddits where topicKeyword like '%{keyword}%'  ORDER BY numberofcomments DESC limit 100'''
        cursor.execute(create_table_query)
        records = cursor.fetchall()
        return records

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)

def getHighestSubredditsbyTopScore(keyword):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()
        create_table_query = f'''select * from subreddits where topicKeyword like '%{keyword}%'  ORDER BY topicScore DESC limit 100'''
        cursor.execute(create_table_query)
        records = cursor.fetchall()
        return records

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)

def getTotalCount(table):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()
        create_table_query = f'''select count(*) from {table}'''
        cursor.execute(create_table_query)
        records = cursor.fetchone()
        return records

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)


def getTotalCountFilteredComments(keyword):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()
        create_table_query = f'''select count(*) from comments where commentBody like '%{keyword}%' '''
        cursor.execute(create_table_query)
        records = cursor.fetchone()
        return records

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)
        

def getTotalCountFilteredSubreddit(keyword):
    """
    docstring
    """
    try:

        connection = psycopg2.connect(user="postgres",
                                      password="poc123",
                                      host="localhost",
                                      port=5555,
                                      database="redditdb")

        cursor = connection.cursor()
        create_table_query = f'''select count(*) from subreddits where topicTitle like '%{keyword}%' '''
        cursor.execute(create_table_query)
        records = cursor.fetchone()
        return records

    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)