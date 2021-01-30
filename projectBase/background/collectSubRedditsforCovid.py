import praw
import database_infrastructure.dbHandler as dbController
from apscheduler.schedulers.background import BackgroundScheduler
import redditController.collectSubredditsForAsync as redditController


def collectSubredditsForCovid():
    redditController.collectSubredditsForCovid('covid')
    redditController.collectSubredditsForCovid('covid19')


def collectAsync():
    print("registering async background job")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=collectSubredditsForCovid,
                      trigger="interval", days=1)
    scheduler.start()
