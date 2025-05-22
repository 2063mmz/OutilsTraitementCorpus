# Projet de scraping de données Allociné
## Présentation du projet  
Ce dépôt contient 8 scripts. Le script `crawler.py` sert à récupérer le contenu du site. Trois scripts de `visualisation_*.py` permettent d’afficher les commentaires, pour avoir des stats plus précises, j’ai aussi nettoyé un peu les textes. `synonym_dict.py` et `augmentation_corpus.py` servent à enrichir le corpus avec la méthode de remplacement par synonymes (SR). Enfin, `modele.py` et `evaluation.py` sont là pour faire le fine-tuning et évaluer du modèle.

Dans ce projet, l’idée c’était de créer un système qui arrive à classifier automatique des sentiments à partir de critiques textuelles. Le besoin auquel je réponds est celui de l’analyse d’opinion appliquée aux critiques de séries, afin d’identifier automatiquement si un avis est positif ou négatif. Pour les donnée, j’ai consulté le fichier `robots.txt` d’Allociné, et il n’interdit pas le crawl de la section critique, donc c’est autorisé. Le fichier CSV contenant les données extraites du site web a été accidentellement mis sur GitHub, mais je l’ai déjà supprimé.

Le sujet que j’ai extrait les critiques de la série _The Last of Us_ sur **Allociné**. J’ai classé les commentaires en positifs et négatifs en fonction des notes (0-5), comme il y avait assez peu de données, je n’ai pas inclus de catégorie neutre. Donc, 1 pour les avis positifs (note ≥ 3.0), 0 pour les avis négatifs (note < 3.0)

La tâche est donc une classification binaire supervisée, à partir de commentaires.

Concernant les **données**, j’ai récupéré les critiques avec le script `crawler.py` (sans API), en respectant les conditions d’accès du site, j’ai ajouté `time.sleep(1)` dans le script pour réduire la fréquence des requêtes. Les données sont ensuite stockées dans un fichier CSV.

Ensuite, j’ai fait des **visualisations** pour voir les mots les plus fréquents dans les commentaires, la longueur des commentaires, et aussi leurs valeurs TF-IDF.

À partir la fréquence, j’ai construit un dictionnaire de synonymes pour **enrichir** mon corpus, j’ai mis en place une augmentation de données via SR (Synonym Replacement) de EDA, en utilisant un dictionnaire de synonymes construit à partir des mots fréquents.

Pour **entraîner** le modèle, j’ai choisi le modèle `BERT (bert-base-multilingual-cased)`, puis, je l’ai fine-tunée sur mon corpus. Le système est ensuite évalué à l’aide de métriques classiques comme l’exactitude et la F-mesure.

Comme les résultats générés par le modèle sont trop volumineux, je n'avais pas suffisamment d'espace sur mon ordinateur pour les ajouter sur GitHub, c'est pourquoi je ne les ai pas téléchargés.
