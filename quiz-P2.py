# Import des librairies Python dont nous avons besoin
import pandas as pd

# Affichage des données du fichier CSV
data = pd.read_csv('quiz-P2.csv')
print(data.head())

# Question 1
VALID_DEPT = [76, 27, 14]
mask = ~data['Dept'].isin(VALID_DEPT)
print('\nAffichage des départements invalides :')
print(data.loc[mask, :])

# Question 2
print('\nVoici le nombre de valeurs manquantes par variable :')
print(data.isnull().sum())

# Question 3
print('\nVoici l\'erreur de conversion en datetime :')
print(data.iloc[250, :])
data['Temps'] = pd.to_datetime(data['Temps'],
                               format='%H:%M:%S', errors='coerce')
print("\nVoici la valeur manquante après conversion en datetime :")
print(data.loc[data['Temps'].isnull(), :])

# Question 4
print('\nAffichage des outliers :')
print(data[['Position', 'Age', 'Temps_secondes']].describe())

# Question 5
print('\nAffichage des doublons :')
print(data.loc[data.duplicated(keep=False), :])

# Question 6
VALID_SEXE = ['M', 'F']
mask = ~data['Sexe'].isin(VALID_SEXE)
print('\nAffichage des sexes invalides :')
print(data.loc[mask, :])
