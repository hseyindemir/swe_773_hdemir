import praw
import database_infrastructure.dbHandler as dbController
from apscheduler.schedulers.background import BackgroundScheduler

def collectCommentsForCovid():
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    topicList = redditGate.comment('covid').controversial("day")
    for topic in topicList:
        topicRecord = {
            "id" : topic.subreddit_id,
            "commentAuthor": str(topic.author),
            "commentLink": topic.permalink,
            "commentBody": topic.body,
            "commentScore": topic.score,
            "commentDate": round((int(topic.created_utc)),0)
        }
        dbController.addRecordToComments(topicRecord)
    dbController.addSearchRecord('covid')


def collectAsyncComments():
    print("registering async background job")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=collectCommentsForCovid, trigger="interval", days=1)
    scheduler.start()