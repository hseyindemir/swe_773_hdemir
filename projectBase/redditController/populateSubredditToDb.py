import praw
import database_infrastructure.dbHandler as dbController
import redditController.redditGate as redditControl
import asyncio
def populateSubReddit(keyword, max):
    redditGate = redditControl.createRedditConnection()
    topicList = redditGate.subreddit(keyword).hot(limit=max)
    resultSet = []
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
        resultSet.append(topicRecord)
        dbController.addRecordToSubreddits(topicRecord)
    dbController.addSearchRecord(keyword)


def populateFirstSubreddits(keyword):
    redditGate = redditControl.createRedditConnection()
    topicList = redditGate.subreddit(keyword).hot(limit=10000)
    resultSet = []
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
        resultSet.append(topicRecord)
        dbController.addRecordToSubreddits(topicRecord)
    dbController.addSearchRecord(keyword)


def populateFirstComments(keyword):
    redditGate = redditControl.createRedditConnection()
    topicList = redditGate.subreddit(keyword).comments(limit=10000)
    resultSet = []
    for topic in topicList:
        topicRecord = {
            "id": topic.subreddit_id,
            "commentAuthor": str(topic.author),
            "commentLink": topic.permalink,
            "commentBody": topic.body,
            "commentScore": topic.score,
            "commentDate": round((int(topic.created_utc)), 0)
        }
        dbController.addRecordToComments(topicRecord)
        resultSet.append(topicRecord)
    dbController.addSearchRecord(keyword)