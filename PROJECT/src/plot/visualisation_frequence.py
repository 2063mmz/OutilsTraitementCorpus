import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt

# Charger le modèle français de spaCy
nlp = spacy.load("fr_core_news_sm")

# Charger vos données de commentaires, supposé qu’il y a deux colonnes : 'text' et 'label' (1 = positif, 0 = négatif)
df = pd.read_csv("comments.csv", header=None)

# Fonction : extraire la fréquence des mots pour une étiquette donnée (0 ou 1)
def frequencies(df, label):
    all_tokens = []
    for text in df[df[2] == label][1]:
        doc_pos = nlp(text)
        tokens = [token.text.lower() for token in doc_pos if token.is_alpha and not token.is_stop]
        all_tokens.extend(tokens)
    return Counter(all_tokens)

# Obtenir la fréquence des mots pour les commentaires positifs et négatifs
pos_freq = frequencies(df, 1)
neg_freq = frequencies(df, 0)

# Extraire les 20 mots les plus fréquents et les visualiser
def plot_freq(counter, title):
    top_words = counter.most_common(20)
    words, freqs = zip(*top_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, freqs)
    plt.xticks(rotation=45)
    plt.title(title)
    plt.ylabel("Fréquence")
    plt.tight_layout()
    plt.show()

plot_freq(pos_freq, "Top 20 mots dans les commentaires POS")
plot_freq(neg_freq, "Top 20 mots dans les commentaires NÉG")
