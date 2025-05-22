import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import spacy

# Utiliser stopwords en français de spacy
nlp = spacy.load('fr_core_news_sm')
stopwords_fr = nlp.Defaults.stop_words

# Lire le fichier CSV
df = pd.read_csv('comments.csv',header=None) 
pos = df[df[2]==1][1]
neg = df[df[2]==0][1]

# Calcul du TF-IDF
# Extraire au maximum 80 mots
vectorizer = TfidfVectorizer(max_features=80, stop_words=list(stopwords_fr)) 
X_pos = vectorizer.fit_transform(pos)
X_neg = vectorizer.fit_transform(neg)

# Conversion 
tfidf_df_pos = pd.DataFrame(X_pos.toarray(), columns=vectorizer.get_feature_names_out())
tfidf_df_neg = pd.DataFrame(X_neg.toarray(), columns=vectorizer.get_feature_names_out())

# Calcul de la moyenne du TF-IDF pour chaque mot
mean_scores_pos = tfidf_df_pos.mean().sort_values(ascending=False).head(15)
mean_scores_neg = tfidf_df_neg.mean().sort_values(ascending=False).head(15)

# Visualisation en utilisant matplotlib
plt.figure(figsize=(10, 6))
plt.barh(mean_scores_pos.index[::-1], mean_scores_pos.values[::-1], color='salmon')
plt.barh(mean_scores_neg.index[::-1], mean_scores_neg.values[::-1], color='gray') 
plt.xlabel('Score moyen TF-IDF')
plt.title('15 mots les plus représentatifs par classe pos-orange et neg-gris (TF-IDF)')
plt.tight_layout()
plt.show()
