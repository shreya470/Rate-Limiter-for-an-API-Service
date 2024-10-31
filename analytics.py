from model import db, SocialMediaPost
from textblob import TextBlob


#db = SQLAlchemy()  # Create a new SQLAlchemy instance

def fetch_analytics(user_id, platform=None, start_time=None, end_time=None):

    query = db.session.query(SocialMediaPost)

    query = query.filter(SocialMediaPost.user_id == user_id)

    if platform:
        query = query.filter(SocialMediaPost.platform == platform)

    if start_time:
        query = query.filter(SocialMediaPost.timestamp >= start_time)
    if end_time:
        query = query.filter(SocialMediaPost.timestamp <= end_time)

    posts = query.all()

    mentions_count = len(posts)
    top_hashtags = extract_top_hashtags(posts)
    sentiment_score = calculate_sentiment(posts)

    return {
        "mentions_count": mentions_count,
        "top_hashtags": top_hashtags,
        "sentiment_score": sentiment_score
    }

def extract_top_hashtags(posts):
    hashtag_counter = {}
    for post in posts:
        hashtags = [word for word in post.content.split() if word.startswith('#')]
        for hashtag in hashtags:
            hashtag_counter[hashtag] = hashtag_counter.get(hashtag, 0) + 1

    sorted_hashtags = sorted(hashtag_counter.items(), key=lambda item: item[1], reverse=True)
    top_hashtags = [hashtag for hashtag, count in sorted_hashtags]
    return top_hashtags


def calculate_sentiment(posts):
    total_sentiment = 0.0
    for post in posts:
        # Use TextBlob to get the polarity score of the content
        blob = TextBlob(post.content)
        total_sentiment += blob.sentiment.polarity  # polarity ranges from -1 to +1

    # Calculate the average sentiment score
    return total_sentiment / len(posts) if posts else 0.0

