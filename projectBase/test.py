import praw
redditGate = praw.Reddit(client_id='GlQ2GmyaogYirw',
                         client_secret='ee_qHpCcpcewxWdDu3cjniI55g8Ivg',
                         user_agent='swe573')
count=0
subreddit = redditGate.submission("covid").collections
for submission in subreddit:
    count=count+1
    print(submission.title)

print(count)