# import des librairies dont nous avons besoin
import pandas as pd
import numpy as np

# chargement et affichage des données
data = pd.read_csv('personnes.csv')
print(data)

# comptabiliser le nombre de valeurs manquantes par variable
print('\nVoici le nombre de valeurs manquantes par variable :')
print(data.isnull().sum())

# afficher l'ensemble des lignes concernées par un doublon sur la variable 'email'
print('\nVoici les lignes concernées par un doublon sur la variable \'email\' :')
print(data.loc[data['email'].duplicated(keep=False), :])

# remplacer les valeurs invalides de la variable 'pays' par les valeurs manquantes
VALID_COUNTRIES = ['France', 'Côte d\'ivoire', 'Madagascar', 'Bénin', 'Allemagne', 'USA']
mask = ~data['pays'].isin(VALID_COUNTRIES)
data.loc[mask, 'pays'] = np.nan
print('\nVoici le tableau modifié (les valeurs invalides de pays sont remplacées '
      'par les valeurs manquantes) :')
print(data)

# l'adresse e-mail doit être unique
data['email'] = data['email'].str.split(',', n=1, expand=True)[0]
print('\nVoici le tableau avec adresse e-mail unique :')
print(data)

# remplacer les tailles invalides par les valeurs manquantes
data['taille'] = data['taille'].str[:-1]
data['taille'] = pd.to_numeric(data['taille'], errors='coerce')
print('\nVoici le tableau modifié (les tailles invalides sont remplacées '
      'par les valeurs manquantes) :')
print(data)

# remplacer les tailles manquantes par la moyenne de la variable 'taille'
data.loc[data['taille'].isnull(), 'taille'] = data['taille'].mean()
print('\nVoici le tableau modifié (les tailles manquantes sont remplacées '
      'par la moyenne de la variable \'taille\') :')
print(data)

# changer le format des dates de naissance
data['date_naissance'] = pd.to_datetime(data['date_naissance'],
                                        format='%d/%m/%Y', errors='coerce')
print('\nVoici le tableau modifié (Les dates de naissance '
      'sont au format YYYY-mm-dd) :')
print(data)
