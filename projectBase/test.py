import praw
redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                         client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                         user_agent='swe573')
count=0
subreddit = redditGate.subreddit('covid').hot(limit=100000)
for submission in subreddit:
    count=count+1
    print(submission.title)

print(count)