import praw


def createRedditConnection():
    """
    docstring
    """
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    return redditGate
