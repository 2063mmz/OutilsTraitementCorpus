import pandas as pd
import matplotlib.pyplot as plt

#  Lire le fichier CSV
df = pd.read_csv('comments.csv', header=None)
texts = df[1]
labels = df[2]

# Calculer la longueur de chaque texte 
lengths = texts.apply(lambda x: len(x.split()))

# Créer la figure
plt.figure(figsize=(10, 10))

# Tracer toutes les barres d'un coup, avec une couleur selon le label : pos → saumon, neg → gris
colors = ['salmon' if label == 1 else 'gray' for label in labels]
plt.barh(range(len(lengths)), lengths.values, color=colors)

# Afficher la valeur (nombre de mots) sur chaque barre
for i, v in enumerate(lengths.values):
    plt.text(v + 0.2, i, str(v), va='center')

# Configurer les axe
plt.xlabel('Nombre de mots')
plt.ylabel('Index dans le CSV')
plt.title('Longueur des textes (chaque ligne du fichier par pos-orange et neg-gris)')
plt.yticks(range(len(lengths)))
plt.tight_layout()
plt.show()
