import pandas as pd
import random
import spacy
import json

# Charger le modèle spacy
nlp = spacy.load("fr_core_news_sm")
stop_words = nlp.Defaults.stop_words

# Charger le dictionnaire de synonymes
with open("synonym_dict.json", "r", encoding="utf-8") as f:
    synonym_dict = json.load(f)

# Fonction pour obtenir les synonymes depuis le dictionnaire
def get_synonyms(word):
    return synonym_dict.get(word, [])

# Fonction de remplacement par synonymes (SR)
def synonym_replacement(words, n):
    new_words = words.copy()
    candidates = [w for w in words if w not in stop_words and w in synonym_dict]
    random.shuffle(candidates)
    replaced = 0
    for word in candidates:
        synonyms = get_synonyms(word)
        if synonyms:
            synonym = random.choice(synonyms)
            new_words = [synonym if w == word else w for w in new_words]
            replaced += 1
        if replaced >= n:
            break
    return new_words

# EDA avec SR seulement
def eda_sr(sentence, alpha_sr=0.1, num_aug=4):
    words = sentence.lower().split()
    words = [w for w in words if w.isalpha()]
    n_sr = max(1, int(alpha_sr * len(words)))
    augmented = []
    for _ in range(num_aug):
        new_words = synonym_replacement(words, n_sr)
        augmented.append(" ".join(new_words))
    return augmented

# Charger le fichier CSV
df = pd.read_csv("comments.csv", header=None)

# Génération des textes augmentés
aug_texts = []
aug_labels = []

for text, label in zip(df[1], df[2]):
    if not isinstance(text, str):
        continue
    augmented = eda_sr(text, alpha_sr=0.2, num_aug=1)
    aug_texts.append(augmented[0])
    aug_labels.append(label)

# Définir les noms de colonnes
df.columns = ["index", "text", "label"]

# Créer un dataframe avec uniquement texte et étiquette
df_orig = df[["text", "label"]].copy()
df_aug = pd.DataFrame({"text": aug_texts, "label": aug_labels})

# Fusionner les deux dataframes
df_all = pd.concat([df_orig, df_aug], ignore_index=True)

# Sauvegarder dans un nouveau fichier CSV
df_all.to_csv("comments_sr_augmented.csv", index=False, encoding="utf-8")
print("Augmentation terminée")
