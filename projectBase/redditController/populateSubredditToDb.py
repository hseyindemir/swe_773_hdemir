import praw
import database_infrastructure.dbHandler as dbController
import redditController.redditGate as redditControl
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


async def populateFirstSubreddits(keyword):
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