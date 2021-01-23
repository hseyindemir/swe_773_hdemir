import praw
import database_infrastructure.dbHandler as dbController
from apscheduler.schedulers.background import BackgroundScheduler


def collectSubredditsForCovid():
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    topicList = redditGate.subreddit('covid').controversial("day")
    for topic in topicList:
        topicRecord = {
            "topicId": topic.id,
            "topicTitle": topic.title,
            "topicCommentCount": topic.num_comments,
            "topicScore": topic.score,
            "isAdult": topic.over_18,
            "topicUpvoteRation": topic.upvote_ratio,
            "topicKeyword": 'covid'
        }
        dbController.addRecordToSubreddits(topicRecord)
    dbController.addSearchRecord('covid')


def collectAsync():
    print("registering async background job")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=collectSubredditsForCovid,
                      trigger="interval", minutes=1)
    scheduler.start()
