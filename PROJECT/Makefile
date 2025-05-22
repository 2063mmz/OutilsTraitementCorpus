PYTHON=python3

# Récupérer les critiques depuis Allociné et les sauvegarder dans data/raw/comments.csv
crawl_neg:
	$(PYTHON) src/process/crawler.py "https://www.allocine.fr/series/ficheserie-26316/critiques/" 100 0 data/raw/comments.csv

crawl_pos:
	$(PYTHON) src/process/crawler.py "https://www.allocine.fr/series/ficheserie-26316/critiques/" 100 1 data/raw/comments.csv

# Visualisation des fréquences de mots à partir du fichier comments.csv
plot_freq:
	$(PYTHON) src/plot/visualisation_frequence.py

# Visualisation des longueurs de commentaires
plot_len:
	$(PYTHON) src/plot/visualisation_longueur.py

# Visualisation des scores TF-IDF
plot_tfidf:
	$(PYTHON) src/plot/visualisation_TFIDF.py

# Générer un dictionnaire de synonymes (pour l'augmentation de données)
synonyms:
	$(PYTHON) src/process/synonym_dict.py data/clean/synonym_dict.json

# Augmenter les données avec remplacement par synonymes
augment:
	$(PYTHON) src/process/augmentation_corpus.py

# Entraîner le modèle BERT (fichier en sortie : ./results/checkpoint-*)
train:
	$(PYTHON) src/model/modele.py

# Évaluer le modèle entraîné (à partir de checkpoint-12)
evaluate:
	$(PYTHON) src/model/evaluation.py

# Exécuter tout le pipeline dans l'ordre logique
all: crawl plot_freq plot_len plot_tfidf synonyms augment train evaluate

# Nettoyer les fichiers intermédiaires et résultats temporaires
clean:
	rm -f data/clean/*.csv
	rm -f comments_sr_augmented.csv
	rm -f synonym_dict.json
	rm -rf results/
	rm -rf eval_tmp/
	rm -f *.png *.svg

.PHONY: crawl plot_freq plot_len plot_tfidf synonyms augment train evaluate all clean

