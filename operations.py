# Import des librairies dont nous avons besoin
import numpy as np
import pandas as pd

# Lire le fichier 'operations.csv'
data = pd.read_csv('operations.csv')
print('Voici les 5 premières lignes du tableau :')
print(data.head())

# 1. Erreurs de type
print('\nVoici les types des différentes variables :')
print(data.dtypes)
print('\nLa variable \'date_operation\' est de type object.')
print('Il faut la convertir en datetime :')
data['date_operation'] = pd.to_datetime(data['date_operation'])
print(data.dtypes)

# 2. Valeurs manquantes
print('\nNombre de valeurs manquantes pour chaque variable :')
print(data.isnull().sum())
print('\nOn affiche les variables qui ont des valeurs manquantes :')
nb_na = data.isnull().sum()
print(nb_na[nb_na > 0])

# Valeurs manquantes pour la variable 'montant'
print('\nValeurs manquantes pour la variable \'montant\' :')
print(data.loc[data['montant'].isnull(), :])
# on stocke le df des valeurs manquantes dans un nouveau df
data_na = data.loc[data['montant'].isnull(),:]
# pour chaque ligne de mon df, on récupère les index (qui ne changent pas au travers du .loc)
for index in data_na.index:
    # calcul du montant à partir des soldes précédents et actuels
    data.loc[index, 'montant'] = data.loc[index+1, 'solde_avt_ope'] - data.loc[index, 'solde_avt_ope']

# Valeur manquante pour la variable 'categorie'
print('\nValeur manquante pour la variable \'categorie\' :')
print(data.loc[data['categ'].isnull(), :])
# On cherche la catégorie qui correspond au libellé de la ligne en question
print('\nRecherche de la catégorie :')
print(data.loc[data['libelle'] == 'PRELEVEMENT XX TELEPHONE XX XX', :])
# On modifie la catégorie de la ligne en question
data.loc[data['categ'].isnull(), 'categ'] = 'FACTURE TELEPHONE'

# 3. Doublons
print('\nAffichage des doublons :')
print(data.loc[data[['date_operation', 'libelle', 'montant', 'solde_avt_ope']].duplicated(keep=False), :])
# On supprime l'une des deux opérations
data.drop_duplicates(subset=['date_operation', 'libelle', 'montant', 'solde_avt_ope'], inplace=True, ignore_index=True)

# 4. Détection d'outliers
print('\nAffichage des informations du dataframe :')
print(data[['montant','solde_avt_ope']].describe())
# récupération de l'index de la transaction à -15000
i = data.loc[data['montant'] == -15000, :].index[0]
# on regarde la transaction précédente et la suivante
print('\nAffichage de la transaction précédente, de la transaction courante et la transaction suivante :')
print(data.iloc[i-1:i+2, :])
# Les soldes nous indiquent une opération de -14.39 et non de -15000.
# Remplaçons donc la valeur aberrante par -14.39
data.loc[data['montant'] == -15000, 'montant'] = -14.39
