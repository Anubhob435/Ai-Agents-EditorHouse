import os
from dotenv import load_dotenv
import praw

# Load environment variables from .env file
load_dotenv()

# Get values from the environment
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

# Initialize PRAW
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

# Step 1: Get top 5 trending posts from Reddit front page (r/all)
trending_posts = list(reddit.subreddit("all").hot(limit=5))

print("🔥 Top Trending Topics:\n")

trending_keywords = []
for i, post in enumerate(trending_posts, start=1):
    keyword = post.title.split(" ")[0:4]  # Use first few words as a simple topic
    topic = " ".join(keyword)
    trending_keywords.append(topic)
    print(f"{i}. {topic}")

print("\n🔍 Searching top 2 posts for each topic...\n")

# Step 2: Search Reddit for each trending topic
all_reddit_data = []  # Collect all data for story generation

for topic in trending_keywords:
    print(f"🔎 Topic: {topic}")
    search_results = reddit.subreddit("all").search(topic, sort="top", time_filter="day", limit=2)
    
    topic_data = {
        "topic": topic,
        "posts": []
    }

    for post in search_results:
        print(f" - {post.title} (r/{post.subreddit}) | 👍 {post.score} upvotes")
        
        # Collect post data
        post_data = {
            "title": post.title,
            "subreddit": str(post.subreddit),
            "score": post.score,
            "comments": []
        }

        # Optional: Print top-level comment as a "sub post"
        post.comments.replace_more(limit=0)
        top_comments = post.comments[:1]
        for comment in top_comments:
            comment_text = comment.body[:150]
            print(f"   💬 Top Comment: {comment_text}...\n")
            post_data["comments"].append(comment_text)
        
        topic_data["posts"].append(post_data)

    all_reddit_data.append(topic_data)
    print("-" * 60)

# Step 3: Generate a story based on all collected Reddit data
print("\n📚 Generating story from Reddit trends...\n")
