import json

synonym_dict = {
    "jeu": ["jeux", "joué", "jeuxvidéo"],
    "trop": ["vraiment", "tellement", "beaucoup"],
    "série": ["émission", "programme", "drame"],
    "mal": ["mauvais", "négatif", "désagréable"],
    "jeux": ["jeu", "joué", "jeuxvidéo"],
    "rien": ["aucun", "néant", "vide"],
    "épisode": ["partie", "segment"],
    "bien": ["top", "positif", "agréable"],
    "ellie": ["l'actrice", "fille", "héroïne"],
    "personnages": ["protagonistes", "individus", "figures"],
    "scènes": ["séquences", "moments", "extraits"],
    "vidéo": ["clip", "jeuxvidéo", "média"],
    "faire": ["réaliser", "produire", "créer"],
    "fille": ["jeune", "ellie", "héroïne"],
    "monde": ["univers", "planète", "réalité"],
    "bella": ["ramzey", "ellie", "actrice"],
    "actrice": ["interprète", "comédienne", "star"],
    "problème": ["souci", "défaut", "erreur"],
    "histoire": ["intrigue", "récit", "scénario"],
    "joué": ["interprété", "exécuté", "représenté"],
    "acteurs": ["héros", "comédiens", "stars"],
    "séries": ["programmes", "contenus", "dramas"],
    "survie": ["vie", "résistance", "lutte"]
}

# save to json
with open("synonym_dict.json", "w", encoding="utf-8") as f:
    json.dump(synonym_dict, f, ensure_ascii=False, indent=2)
