import praw
import json
import os
import time
from typing import List, Dict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Le fichier de configuration
def load_config() -> Dict:
     return {
        "client_id": "7ni1gEKaRTxgsgKdBjO4Lw",
        "client_secret": "iNHYSIznBqCxH36azpr1yclUVxsEtA",
        "user_agent": "RealisticLeg2210"
    }

def collect_reddit(sub_name:str) -> List[Dict]:
    # Utiliser la configuration
    config = load_config()
    reddit = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        user_agent=config["user_agent"]
    )

    subreddit = reddit.subreddit(sub_name)

    # Récupérer les 20  posts qui sont plus populaires
    posts = []
    for post in subreddit.hot(limit=20):
        '''
        Limiter la fréquence des requêtes. Cela signifie faire une pause de 2 secondes après chaque requête, 
        afin de maintenir la fréquence en dessous de 30 requêtes par minute.
        '''
        time.sleep(2)
        if post.selftext.strip() != "":
            post_data = {
                "title": post.title,
                "author": str(post.author),
                "content": post.selftext,
                "score": post.score,
                "num_comments": post.num_comments,
                "url": post.url
            }
            posts.append(post_data)
    return posts

def save_data(data: List[Dict], save_path: Path) -> str:
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return str(save_path.absolute())

def main():
    # Dossier de sauvegarde
    PROJECT_ROOT = Path(__file__).parent.parent.parent  
    SAVE_DIR = PROJECT_ROOT / "data" / "raw"        
    SAVE_FILE = "severance_posts.json"                 
  

    posts = collect_reddit("SeveranceAppleTVPlus")
    if not posts:
        print("Aucune donnée valide n'a été récupérée")
        return
    
    save_path = SAVE_DIR / SAVE_FILE
    saved_path = save_data(posts, save_path)
    print(f"{len(posts)} éléments ont été récupérés{saved_path}")

if __name__ == "__main__":
    main()