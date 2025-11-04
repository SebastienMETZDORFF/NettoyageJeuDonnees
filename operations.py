# Import des librairies dont nous avons besoin
import pandas as pd
import matplotlib.pyplot as plt

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

# Diagramme en secteurs
data['categ'].value_counts(normalize=True).plot(kind='pie')
# Cette ligne assure que le pie chart est un cercle plutôt qu'une ellipse
plt.axis('equal')
plt.show()

# Diagramme en tuyaux d'orgues
data['categ'].value_counts(normalize=True).plot(kind='bar')
plt.show()

# Diagramme en bâtons
data['quart_mois'] = [int((jour-1)*4/31)+1 for jour in data['date_operation'].dt.day]
data['quart_mois'].value_counts(normalize=True).plot(kind='bar', width=0.1)
plt.show()

# Histogramme
data[data.montant.abs() < 100]['montant'].hist(density=True, bins=20)
plt.show()

# Variable 'quart_mois' sous forme de tableau
effectifs = data['quart_mois'].value_counts()
modalites = effectifs.index # L'index de effectifs contient des modalités
tab = pd.DataFrame(modalites, columns=['quart_mois']) # Création du tableau à partir des modalités
tab['n'] = effectifs.values
tab['f'] = tab['n'] / len(data) # len(data) renvoie la taille de l'échantillon
tab = tab.sort_values('quart_mois') # Tri des valeurs de la variable X (croissant)
tab['F'] = tab['f'].cumsum() # cumsum calcule la somme cumulée
print('\nVoici le tableau de la variable \'quart_mois\' :')
print(tab)
