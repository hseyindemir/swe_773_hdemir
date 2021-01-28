import database_infrastructure.dbHandler as dbController
import praw

def collectSubredditsForCovid(keyword):
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    topicList = redditGate.subreddit(keyword).hot(limit=5000)
    for topic in topicList:
        topicRecord = {
            "topicId": topic.id,
            "topicTitle": topic.title,
            "topicCommentCount": topic.num_comments,
            "topicScore": topic.score,
            "isAdult": topic.over_18,
            "topicUpvoteRation": topic.upvote_ratio,
            "topicKeyword": keyword
        }
        dbController.addRecordToSubreddits(topicRecord)
    dbController.addSearchRecord(keyword)