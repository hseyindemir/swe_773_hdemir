from apscheduler.schedulers.background import BackgroundScheduler
import background.collectCommentsforCovid as covidDailyJobComments
import background.collectSubRedditsforCovid as covidDailyJob
from textblob import TextBlob
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from flask import Flask, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import praw
import redditController.redditGate as redditControl
import redditController.populateSubredditToDb as redditLoader
import json
import resources
import database_infrastructure.dbHandler as dbController
import sentiment.tokenizeController as wordTokenizer
import nltk
import string
from flask_cors import CORS
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)


@app.route('/')
def index():
    f = open('./resources/swagger.json',)
    data = json.load(f)
    return data


@app.route('/welcome/')
def welcome_render():
    dbhost = "fgsdfsd"
    return render_template("base.html", message=dbhost)


@app.route('/populars/<string:keyword>/')
def popular_by_word(keyword):
    redditGate = redditControl.createRedditConnection()
    topicList = redditGate.subreddit(keyword).top("all")
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
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/populars/<string:keyword>/<int:max>')
def popular_by_word_limit(keyword, max):
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
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/comments/<string:keyword>/')
def comments_by_topic_default(keyword):
    redditGate = redditControl.createRedditConnection()
    topicList = redditGate.subreddit(keyword).comments(limit=10)
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
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/comments/<string:keyword>/<int:max>')
def comments_by_topic(keyword, max):
    redditGate = redditControl.createRedditConnection()
    topicList = redditGate.subreddit(keyword).comments(limit=max)
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
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/hitsrecently/')
def get_searchs():
    resultSet = dbController.getHits()
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/topsubredditscomments/<string:keyword>')
def get_subreddits_by_comments(keyword):
    resultSet = dbController.getHighestSubredditsbyTopComments(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_word = nltk.word_tokenize(resultJsonParsed)
    print(tokenized_word)
    fdist = nltk.FreqDist(tokenized_word)
    print(fdist.most_common(2))
    return resultJsonParsed


@app.route('/topsubredditsscore/<string:keyword>')
def get_subreddits_by_score(keyword):
    resultSet = dbController.getHighestSubredditsbyTopScore(keyword)
    
    redditModel=[]
    for record in resultSet:
        topicModelRecord={
            "topicTitle" : record[1],
            "topicScore" : record[2]
        }
        redditModel.append(topicModelRecord)
    redditModel = json.dumps(redditModel, sort_keys=True, indent=4)
    return redditModel

@app.route('/topupvotereddits/<string:keyword>')
def get_subreddits_by_upvote(keyword):
    resultSet = dbController.getHighestSubredditsbyTopUpvote(keyword)
    
    redditModel=[]
    for record in resultSet:
        topicModelRecord={
            "topicTitle" : record[0],
            "upvoteRatio" : record[1]
        }
        redditModel.append(topicModelRecord)
    redditModel = json.dumps(redditModel, sort_keys=True, indent=4)
    return redditModel

@app.route('/totalsinreddit/')
def get_reddit_counts():
    totalComments = dbController.getTotalCount('comments')
    totalSubreddit = dbController.getTotalCount('subreddits')
    countModel = {
        "totalComment": totalComments,
        "totalSubreddit": totalSubreddit
    }
    resultJsonParsed = json.dumps(countModel, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/totalsinredditfiltered/<string:keyword>')
def get_reddit_counts_filtered(keyword):
    from nltk.tokenize import sent_tokenize
    redditLoader.populateSubReddit(keyword=keyword,max=1000)
    totalComments = dbController.getTotalCountFilteredComments(keyword)
    totalSubreddit = dbController.getTotalCountFilteredSubreddit(keyword)
    resultSet = dbController.getSubRedditswhole(keyword)
    resultSetJson = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_text = sent_tokenize(resultSetJson)
    scoreAnalysis = []
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        sentimentRecord = {
            "positivity": analysis[1],
        }
        scoreAnalysis.append(sentimentRecord)
    totalLengt=len(scoreAnalysis)
    totalValues=(sum(item['positivity'] for item in scoreAnalysis))
    averageScore = totalValues/totalLengt
    resultSet = dbController.getCommentwhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_text = sent_tokenize(resultJsonParsed)
    scoreAnalysis = []
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        sentimentRecord = {
            "positivity": analysis[1],
        }
        scoreAnalysis.append(sentimentRecord)
    totalLengt=len(scoreAnalysis)
    totalValues=(sum(item['positivity'] for item in scoreAnalysis))
    averageScoreComment = (totalValues/totalLengt)
    countModel = {
        "totalComment": totalComments,
        "totalSubreddit": totalSubreddit,
        "averageScore" : "{:.2f}".format(averageScore),
        "averageScoreComment":  "{:.2f}".format(averageScoreComment)
        
    }
    resultJsonParsed = json.dumps(countModel, sort_keys=True, indent=4)
    return resultJsonParsed

@app.route('/totalsinredditv2/<string:keyword>')
def get_reddit_totals_v2(keyword):
    from nltk.tokenize import sent_tokenize
    redditLoader.populateSubReddit(keyword=keyword,max=100)
    totalComments = dbController.getTotalCountFilteredComments(keyword)
    totalSubreddit = dbController.getTotalCountFilteredSubreddit(keyword)
    resultSet = dbController.getSubRedditswhole(keyword)
    resultSetJson = json.dumps(resultSet, sort_keys=True, indent=4)
    resultSetHighReddit = dbController.getHighestSubredditsbyTopScore(keyword)
    redditModel=[]
    for record in resultSetHighReddit:
        topicModelRecord={
            "topicTitle" : record[1],
            "topicScore" : record[2]
        }
        redditModel.append(topicModelRecord)
    tokenized_text = sent_tokenize(resultSetJson)
    scoreAnalysis = []
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        sentimentRecord = {
            "positivity": analysis[1],
        }
        scoreAnalysis.append(sentimentRecord)
    totalLengt=len(scoreAnalysis)
    totalValues=(sum(item['positivity'] for item in scoreAnalysis))
    averageScore = totalValues/totalLengt
    resultSet = dbController.getCommentwhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_text = sent_tokenize(resultJsonParsed)
    scoreAnalysis = []
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        sentimentRecord = {
            "positivity": analysis[1],
        }
        scoreAnalysis.append(sentimentRecord)
    totalLengt=len(scoreAnalysis)
    totalValues=(sum(item['positivity'] for item in scoreAnalysis))
    averageScoreComment = (totalValues/totalLengt)
    resultSetUpvote = dbController.getHighestSubredditsbyTopUpvote(keyword)
    
    redditModelUpvote=[]
    for record in resultSetUpvote:
        topicModelRecord={
            "topicTitle" : record[0],
            "upvoteRatio" : record[1]
        }
        redditModelUpvote.append(topicModelRecord)
    import nltk
    from nltk.corpus import stopwords
    resultSetFrequency = dbController.getSubRedditswhole(keyword)
    resultJsonParsed2 = json.dumps(resultSetFrequency, sort_keys=True, indent=4)
    tokens_without_sw=wordTokenizer.convertResultToToknizeFormat(resultJsonParsed2)
    fdist = nltk.FreqDist(tokens_without_sw)
    keywordList=[]
    for record in fdist.most_common(10):
        keywordRecord={
            "keyword" : record[0],
            "count" : record[1]
        }
        keywordList.append(keywordRecord)
    countModel = {
        "totalComment": totalComments,
        "totalSubreddit": totalSubreddit,
        "averageScore" : "{:.2f}".format(averageScore),
        "averageScoreComment":  "{:.2f}".format(averageScoreComment),
        "highReddits" : redditModel,
        "upvoteReddits" : redditModelUpvote,
        "keywordList" : keywordList
        
    }
    resultJsonParsed = json.dumps(countModel, sort_keys=True, indent=4)
    return resultJsonParsed

@app.route('/mostusedwordsinsubreddits/<string:keyword>')
def get_most_pupulars(keyword):
    import nltk
    from nltk.corpus import stopwords
    resultSet = dbController.getSubRedditswhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokens_without_sw=wordTokenizer.convertResultToToknizeFormat(resultJsonParsed)
    fdist = nltk.FreqDist(tokens_without_sw)
    keywordList=[]
    for record in fdist.most_common(10):
        keywordRecord={
            "keyword" : record[0],
            "count" : record[1]
        }
        keywordList.append(keywordRecord)
    keywordList=json.dumps(
        keywordList, sort_keys=True, indent=4)
        
    return keywordList


@app.route('/mostusedwordsincomments/<string:keyword>')
def get_most_pupulars_comments(keyword):
    import nltk
    from nltk.corpus import stopwords
    resultSet = dbController.getCommentwhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokens_without_sw=wordTokenizer.convertResultToToknizeFormat(resultJsonParsed)
    fdist = nltk.FreqDist(tokens_without_sw)
    resultJsonParsed2 = json.dumps(
        fdist.most_common(100), sort_keys=True, indent=4)
    return resultJsonParsed2


@app.route('/commentSentiments/<string:keyword>')
def get_positives_negatives(keyword):
    from nltk.tokenize import sent_tokenize
    resultSet = dbController.getCommentwhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_text = sent_tokenize(resultJsonParsed)
    scoreAnalysis = []
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        print(analysis)
        sentimentRecord = {
            "positivity": analysis[1],
            "comment": tex
        }
        scoreAnalysis.append(sentimentRecord)
    jsonAnalysis = json.dumps(scoreAnalysis, sort_keys=True, indent=4)
    return jsonAnalysis


@app.route('/topicsentiments/<string:keyword>')
def get_positives_negatives_topic(keyword):
    from nltk.tokenize import sent_tokenize
    resultSet = dbController.getSubRedditswhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_text = sent_tokenize(resultJsonParsed)
    scoreAnalysis = []
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        print(analysis)
        sentimentRecord = {
            "positivity": analysis[1],
            "comment": tex
        }
        scoreAnalysis.append(sentimentRecord)
    jsonAnalysis = json.dumps(scoreAnalysis, sort_keys=True, indent=4)
    return jsonAnalysis


if __name__ == '__main__':
    SWAGGER_URL = '/api/docs'
    API_URL = 'http://localhost:5000'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        },
    )
    #covidDailyJob.collectAsync()
    #covidDailyJobComments.collectAsyncComments()
    CORS(app)
    app.register_blueprint(swaggerui_blueprint)
    app.run(host="0.0.0.0", port=5000)
