import requests
from bs4 import BeautifulSoup
import sys
import time
import csv
import argparse

# Commande: python crawler.py https://www.allocine.fr/series/ficheserie-26316/critiques/ 500 0 comments.csv
# 500 -> nb de commantaire minimale, 0 -> class de label, pos -> 1, neg -> 0


def fetch_reviews(movie_url, min_length, label_type, total_critiques):
    # Utiliser un 'user-agent' pour éviter d’être bloqué
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    comments_data = []
    page = 1
    collection_critiques = 0
    # Utiliser une boucle while
    while True:
        url = f"{movie_url}?page={page}"
        print(f"Téléchargement de la page {page} : {url}")
        # Vérifier si la pagepeut être demandée correctement; sinon, sortir de la boucle
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Impossible d’accéder à la page (code {response.status_code})")
            break
        # Utiliser BeautifulSoup pour examiner le résultat de l’analyse
        soup = BeautifulSoup(response.text, 'html.parser')
        # Rechercher tous les blocs de critiques correspondants sur la page, c'est le class: 'hred review-card cf'
        review_cards = soup.find_all('div', class_='hred review-card cf')

        if not review_cards:
            print("Plus de critiques trouvées.")
            break

        for card in review_cards:
            # Lire la note de chaque critique
            note_tag = card.find('span', class_='stareval-note')
            # Si la critique n’a pas de note, l’ignorer
            if not note_tag:
                continue
            # Convertir en float et normaliser la ponctuation
            note = float(note_tag.get_text(strip=True).replace(',', '.'))
            # Extraire des critiques
            comment_tag = card.find('div', class_='content-txt review-card-content')
            if not comment_tag:
                continue
            comment = comment_tag.get_text(strip=True)
            # Filtrer les critiques selon le label, pour mieux entraîner le modèle, n’utilise pas la catégorie "neutre", les avis sont séparés en deux classes.
            if len(comment) >= min_length:
                if note >= 3.0:
                    label = '1'
                else:
                    label = '0'

                if label == label_type:
                    comments_data.append([note, comment, label])
                    collection_critiques += 1

                    if collection_critiques >= total_critiques:
                        print(f"{total_critiques} critiques récupérées, arrêt du programme.")
                        return comments_data

        page += 1
        time.sleep(1)

    return comments_data

# Écrire dans le fichier csv
def save_to_csv(comments_data, file):
    with open(file, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        if not file:
            writer.writerow(['Note', 'Comment', 'Class'])
        writer.writerows(comments_data)
    print(f"Les critiques ont été enregistrées dans le fichier {file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Allociné scraper : récupère les critiques par label")

    parser.add_argument("url", help="URL de la page des critiques")
    parser.add_argument("min_length", type=int, help="Longueur minimale de chaque commentaire")
    parser.add_argument("label_type", choices=["1", "0"], help="Filtrer des critiques par label, pos -> 1, neg -> 0")
    parser.add_argument("output_csv", help="Fichier CSV de sortie") 
    parser.add_argument("--total_critiques", type=int, default=10, help="Nombre total de critiques à récupérer (par défaut 10)")
    args = parser.parse_args()

    tous_comments = fetch_reviews(
        movie_url=args.url.strip('/'),
        min_length=args.min_length,
        label_type=args.label_type,
        total_critiques=args.total_critiques
    )
    print(f"\nTotal de critiques récupérées : {len(tous_comments)}")
    save_to_csv(tous_comments, args.output_csv)
