import praw
from praw.models import MoreComments



def get_text_appearances(postLimit):
    print(f"Starting to collect data from {postLimit} posts...")

    subreddit = "EldenRing"
    reddit = praw.Reddit(client_id='KxbZpLF4CrA7kA', client_secret='9yuiJwOQmu0pj0HV6p6k-dTIB4wtFw', user_agent='post-data-analyzer')

    # redditPosts = reddit.subreddit(subreddit).top(limit=postLimit)
    redditPosts = reddit.subreddit(subreddit).new(limit=postLimit)
    print(f"Retrieved all posts. Starting to retrieve comments from posts...")
    postList = list()

    i = 1
    for post in redditPosts:
        postList.append(get_text_appearances_from_post(post))
        print(f"    Retrieved post comments {i} /  {postLimit}", flush=True)
        i += 1

    return postList

def get_text_appearances_from_post(post):

    comments = list()

    for comment in post.comments.list():
        if isinstance(comment, MoreComments):
            continue
        comments.append(comment_to_text_appearance(comment))
    
    return (post_to_text_appearance(post), comments)


def post_to_text_appearance(post):
    return {
        "id": post.id,
        "is_post": True,
        "text": post.title + "\n" + post.selftext,
        "author": str(post.author),
        "score": post.score,
        "created_utc": post.created_utc,
        "link": post.permalink
    }

def comment_to_text_appearance(comment):
    return {
        "id": comment.id,
        "is_post": False,
        "text": comment.body,
        "author": str(comment.author),
        "score": comment.score,
        "created_utc": comment.created_utc,
        "link": comment.permalink
    }
