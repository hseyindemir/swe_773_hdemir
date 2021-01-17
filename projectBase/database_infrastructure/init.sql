CREATE TABLE public.subreddits (
    id varchar(1000) primary key,
    topicTitle varchar(1000),
    topicScore integer,
    numberofComments integer,
    isAdult boolean,
    upVoteRatio float,
    topicKeyword varchar(1000)
);


CREATE TABLE public.comments (
    id varchar(1000),
    commentAuthor varchar(1000),
    commentLink varchar(1000),
    commentScore integer,
    commentDate bigint
);


CREATE TABLE public.search_requests (
    search_keyword varchar(1000),
    recordDate timestamp without time zone DEFAULT now()
);

create index CONCURRENTLY idx_topic_score_subreddits on subreddits (topicScore);
create index CONCURRENTLY idx_comments_date on comments (commentDate);