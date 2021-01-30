# Install application via docker


* docker build -t reddit_pg_container ./database_infrastructure
* docker run -d --name reddit_db -p 5432:5432 reddit_pg_container
* docker build -t swe573_reddit:v3 .
* docker run -dit --rm -p 5000:5000 --name swe573_backend --link reddit_db swe573_reddit:v3