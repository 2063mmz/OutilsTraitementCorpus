import praw
import json
import os
import time
from typing import List, Dict
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Le fichier de configuration
def load_config() -> dict:
     return {
        "client_id": os.getenv("REDDIT_CLIENT_ID"),
        "client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
        "user_agent": os.getenv("REDDIT_USER_AGENT")
    }

def collect_reddit(sub_name:str) -> List[dict]:
    # Utiliser la configuration
    reddit = praw.Reddit(**load_config())
    posts = []
    for post in reddit.subreddit(sub_name).hot(limit=20):
        time.sleep(2)
        if post.selftext.strip():
            posts.append({
                "title": post.title,
                "author": str(post.author),
                "content": post.selftext,
                "score": post.score,
                "num_comments": post.num_comments,
                "url": post.url
            })
    return posts

def save_data(data: list) -> str:
    save_dir = PROJECT_ROOT / "data" / "raw"
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / "severance_posts.json"
    
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return str(save_path)

def main():
    try:
        posts = collect_reddit("SeveranceAppleTVPlus")
        saved_path = save_data(posts)
        print(f"{len(posts)} éléments ont été récupérés{saved_path}")
    except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()