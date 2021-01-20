from flask import Flask, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import praw
import json
import resources
import database_infrastructure.dbHandler as dbController
import nltk
import string
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from textblob import TextBlob

app = Flask(__name__)


@app.route('/')
def index():
    f = open('./resources/swagger.json',)
    data = json.load(f)
    return data


@app.route('/welcome/')
def welcome_render():
    dbhost="fgsdfsd"
    return render_template("base.html", message=dbhost)


@app.route('/populars/<string:keyword>/')
def popular_by_word(keyword):
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    topicList = redditGate.subreddit(keyword).hot(limit=19)
    resultSet = []
    for topic in topicList:
        topicRecord = {
            "topicId" : topic.id,
            "topicTitle": topic.title,
            "topicCommentCount": topic.num_comments,
            "topicScore": topic.score,
            "isAdult": topic.over_18,
            "topicUpvoteRation" : topic.upvote_ratio,
            "topicKeyword" : keyword
        }
        resultSet.append(topicRecord)
        dbController.addRecordToSubreddits(topicRecord)
    dbController.addSearchRecord(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/populars/<string:keyword>/<int:max>')
def popular_by_word_limit(keyword, max):
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    topicList = redditGate.subreddit(keyword).hot(limit=max)
    resultSet = []
    for topic in topicList:
        topicRecord = {
            "topicId" : topic.id,
            "topicTitle": topic.title,
            "topicCommentCount": topic.num_comments,
            "topicScore": topic.score,
            "isAdult": topic.over_18,
            "topicUpvoteRation" : topic.upvote_ratio,
            "topicKeyword" : keyword
        }
        resultSet.append(topicRecord)
        dbController.addRecordToSubreddits(topicRecord)
    dbController.addSearchRecord(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed

@app.route('/comments/<string:keyword>/')
def comments_by_topic_default(keyword):
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    topicList = redditGate.subreddit(keyword).comments(limit=10)
    resultSet = []
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
        resultSet.append(topicRecord)
    dbController.addSearchRecord(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed

@app.route('/comments/<string:keyword>/<int:max>')
def comments_by_topic(keyword, max):
    redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                             client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                             user_agent='swe573')
    topicList = redditGate.subreddit(keyword).comments(limit=max)
    resultSet = []
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
    tokenized_word=nltk.word_tokenize(resultJsonParsed)
    print(tokenized_word)
    fdist = nltk.FreqDist(tokenized_word)
    print(fdist.most_common(2))
    return resultJsonParsed

@app.route('/topsubredditsscore/<string:keyword>')
def get_subreddits_by_score(keyword):
    resultSet = dbController.getHighestSubredditsbyTopScore(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    return resultJsonParsed

@app.route('/totalsinreddit/')
def get_reddit_counts():
    totalComments = dbController.getTotalCount('comments')
    totalSubreddit = dbController.getTotalCount('subreddits')
    countModel={
        "totalComment": totalComments,
        "totalSubreddit" : totalSubreddit
    }
    resultJsonParsed = json.dumps(countModel, sort_keys=True, indent=4)
    return resultJsonParsed

@app.route('/totalsinredditfiltered/<string:keyword>')
def get_reddit_counts_filtered(keyword):
    totalComments = dbController.getTotalCountFilteredComments(keyword)
    totalSubreddit = dbController.getTotalCountFilteredSubreddit(keyword)
    countModel={
        "totalComment": totalComments,
        "totalSubreddit" : totalSubreddit
    }
    resultJsonParsed = json.dumps(countModel, sort_keys=True, indent=4)
    return resultJsonParsed


@app.route('/mostsimilars/<string:keyword>')
def get_most_pupulars(keyword):
    import nltk 
    from nltk.corpus import stopwords
    resultSet = dbController.getSubRedditswhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    all_stopwords = stopwords.words('english')
    all_stopwords.append('[')
    all_stopwords.append(',')
    all_stopwords.append(']')
    all_stopwords.append('``')
    all_stopwords.append("''")
    all_stopwords.append('?')
    all_stopwords.append('(')
    all_stopwords.append(')')
    all_stopwords.append(':')
    all_stopwords.append('I')
    all_stopwords.append('.')
    all_stopwords.append('-')
    all_stopwords.append("`")
    all_stopwords.append("*")
    all_stopwords.append( "\\")
    all_stopwords.append("...")
    all_stopwords.append("\\n")
    text_tokens = nltk.word_tokenize(resultJsonParsed)
    tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    print(tokens_without_sw)
    fdist = nltk.FreqDist(tokens_without_sw)
    print(fdist.most_common(100))
    resultJsonParsed2 = json.dumps(fdist.most_common(100), sort_keys=True, indent=4)
    return resultJsonParsed2

@app.route('/mostsimilarsComments/<string:keyword>')
def get_most_pupulars_comments(keyword):
    import nltk 
    from nltk.corpus import stopwords
    resultSet = dbController.getCommentwhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    all_stopwords = stopwords.words('english')
    all_stopwords.append('[')
    all_stopwords.append(',')
    all_stopwords.append(']')
    all_stopwords.append('``')
    all_stopwords.append("''")
    all_stopwords.append('?')
    all_stopwords.append('(')
    all_stopwords.append(')')
    all_stopwords.append(':')
    all_stopwords.append('I')
    all_stopwords.append('.')
    all_stopwords.append('-')
    all_stopwords.append("`")
    all_stopwords.append("*")
    all_stopwords.append( "\\")
    all_stopwords.append("...")
    all_stopwords.append("\\n")
    text_tokens = nltk.word_tokenize(resultJsonParsed)
    tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    print(tokens_without_sw)
    fdist = nltk.FreqDist(tokens_without_sw)
    print(fdist.most_common(100))
    resultJsonParsed2 = json.dumps(fdist.most_common(100), sort_keys=True, indent=4)
    return resultJsonParsed2


@app.route('/commentSentiments/<string:keyword>')
def get_positives_negatives(keyword):
    from nltk.tokenize import sent_tokenize
    resultSet = dbController.getCommentwhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_text=sent_tokenize(resultJsonParsed)
    scoreAnalysis=[]
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        print(analysis)
        sentimentRecord={
            "positivity" : analysis[1],
            "comment" : tex
        }
        scoreAnalysis.append(sentimentRecord)
    jsonAnalysis = json.dumps(scoreAnalysis, sort_keys=True, indent=4)
    return jsonAnalysis

@app.route('/topicsentiments/<string:keyword>')
def get_positives_negatives_topic(keyword):
    from nltk.tokenize import sent_tokenize
    resultSet = dbController.getSubRedditswhole(keyword)
    resultJsonParsed = json.dumps(resultSet, sort_keys=True, indent=4)
    tokenized_text=sent_tokenize(resultJsonParsed)
    scoreAnalysis=[]
    for tex in tokenized_text:
        analysis = TextBlob(tex).sentiment
        print(analysis)
        sentimentRecord={
            "positivity" : analysis[1],
            "comment" : tex
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

    app.register_blueprint(swaggerui_blueprint)
    app.run(host="0.0.0.0", port=5000)
