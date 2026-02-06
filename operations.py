# Import des librairies dont nous avons besoin
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

# Lire le fichier 'operations.csv'
data = pd.read_csv('operations.csv')
'''print('Voici les 5 premières lignes du tableau :')
print(data.head())

# 1. Erreurs de type
print('\nVoici les types des différentes variables :')
print(data.dtypes)
print('\nLa variable \'date_operation\' est de type object.')
print('Il faut la convertir en datetime :')'''
data['date_operation'] = pd.to_datetime(data['date_operation'])
'''print(data.dtypes)

# 2. Valeurs manquantes
print('\nNombre de valeurs manquantes pour chaque variable :')
print(data.isnull().sum())
print('\nOn affiche les variables qui ont des valeurs manquantes :')
nb_na = data.isnull().sum()
print(nb_na[nb_na > 0])

# Valeurs manquantes pour la variable 'montant'
print('\nValeurs manquantes pour la variable \'montant\' :')
print(data.loc[data['montant'].isnull(), :])'''
# on stocke le df des valeurs manquantes dans un nouveau df
data_na = data.loc[data['montant'].isnull(),:]
# pour chaque ligne de mon df, on récupère les index (qui ne changent pas au travers du .loc)
for index in data_na.index:
    # calcul du montant à partir des soldes précédents et actuels
    data.loc[index, 'montant'] = data.loc[index+1, 'solde_avt_ope'] - data.loc[index, 'solde_avt_ope']

'''# Valeur manquante pour la variable 'categorie'
print('\nValeur manquante pour la variable \'categorie\' :')
print(data.loc[data['categ'].isnull(), :])
# On cherche la catégorie qui correspond au libellé de la ligne en question
print('\nRecherche de la catégorie :')
print(data.loc[data['libelle'] == 'PRELEVEMENT XX TELEPHONE XX XX', :])'''
# On modifie la catégorie de la ligne en question
data.loc[data['categ'].isnull(), 'categ'] = 'FACTURE TELEPHONE'

'''# 3. Doublons
print('\nAffichage des doublons :')
print(data.loc[data[['date_operation', 'libelle', 'montant', 'solde_avt_ope']].duplicated(keep=False), :])'''
# On supprime l'une des deux opérations
data.drop_duplicates(subset=['date_operation', 'libelle', 'montant', 'solde_avt_ope'], inplace=True, ignore_index=True)

'''# 4. Détection d'outliers
print('\nAffichage des informations du dataframe :')
print(data[['montant','solde_avt_ope']].describe())
# récupération de l'index de la transaction à -15000
i = data.loc[data['montant'] == -15000, :].index[0]
# on regarde la transaction précédente et la suivante
print('\nAffichage de la transaction précédente, de la transaction courante et la transaction suivante :')
print(data.iloc[i-1:i+2, :])'''
# Les soldes nous indiquent une opération de -14.39 et non de -15000.
# Remplaçons donc la valeur aberrante par -14.39
data.loc[data['montant'] == -15000, 'montant'] = -14.39

'''# Diagramme en secteurs
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

# Je découvre les mesures de tendance centrale
print('Mode :', data['montant'].mode(), '\n')
print('Moyenne :', data['montant'].mean(), '\n')
print('Médiane :', data['montant'].median())

# Pour avoir des montants d'opérations plus homogènes, il serait intéressant
# de calculer ces mesures pour chaque catégorie d'opération
for cat in data['categ'].unique():
    subset = data.loc[data['categ'] == cat, :] # Création du sous-échantillon
    print('-'*20)
    print(cat)
    print('Mode :', subset['montant'].mode(), '\n')
    print('Moyenne :', subset['montant'].mean(), '\n')
    print('Médiane :', subset['montant'].median(), '\n')
    subset['montant'].hist() # Crée l'histogramme
    plt.show() # Affiche l'histogramme'''

'''# Je découvre les mesures de dispersion
print('Variance empirique biaisée :', data['montant'].var(), '\n')
print('Variance empirique sans biais :', data['montant'].var(ddof=0), '\n')
print('Ecart-type empirique biaisée :', data['montant'].std(), '\n')
print('Coefficient de variation :', data['montant'].std() / data['montant'].mean(), '\n')
print('Ecart-type empirique sans biais :', data['montant'].std(ddof=0), '\n')

# Boîte à moustaches
data.boxplot(column='montant', vert=False)
plt.show()

# On reprend le code du chapitre précédent et on ajoute pour chaque catégorie : l'écart-type,
# la variance, un histogramme et une boîte à moustaches des montants
for cat in data['categ'].unique():
    subset = data.loc[data['categ'] == cat, :]
    print('-'*20)
    print(cat)
    print('Mode :', subset['montant'].mode(), '\n')
    print('Moyenne :', subset['montant'].mean(), '\n')
    print('Médiane :', subset['montant'].median(), '\n')
    print('Variance :', subset['montant'].var(ddof=0), '\n')
    print('Ecart-type :', subset['montant'].std(ddof=0), '\n')
    subset['montant'].hist()
    plt.show()
    subset.boxplot(column='montant', vert=False)
    plt.show()'''

'''# Je découvre les mesures de forme
# Calcul du skewness
print('Skewness :', data['montant'].skew())
# Calcul du kurtosis
print('Kurtosis :', data['montant'].kurtosis())
# Calcul du skewness empirique et du kurtosis empirique
# pour chaque catégorie
for cat in data['categ'].unique():
    subset = data[data['categ'] == cat]
    print('-'*20)
    print(cat)
    print('Moyenne :\n', subset['montant'].mean())
    print('Médiane:\n', subset['montant'].median())
    print('Mode :\n', subset['montant'].mode())
    print('Variance :\n', subset['montant'].var(ddof=0))
    print('Ecart-type :\n', subset['montant'].std(ddof=0))
    print('Skewness :\n', subset['montant'].skew())
    print('Kurtosis :\n', subset['montant'].kurtosis())
    subset['montant'].hist()
    plt.show()
    subset.boxplot(column="montant", vert=False)
    plt.show()'''

'''# Je découvre les mesures de concentration
depenses = data[data['montant'] < 0]
dep = -depenses['montant'].values
n = len(dep)
lorenz = np.cumsum(np.sort(dep)) / dep.sum()
lorenz = np.append([0],lorenz) # La courbe de Lorenz commence à 0

xaxis = np.linspace(0-1/n,1+1/n,n+1) #Il y a un segment de taille n pour chaque individu, plus 1 segment supplémentaire d'ordonnée 0. Le premier segment commence à 0-1/n, et le dernier termine à 1+1/n.
plt.plot(xaxis,lorenz,drawstyle='steps-post')
plt.show()

AUC = (lorenz.sum() -lorenz[-1]/2 -lorenz[0]/2)/n # Surface sous la courbe de Lorenz. Le premier segment (lorenz[0]) est à moitié en dessous de 0, on le coupe donc en 2, on fait de même pour le dernier segment lorenz[-1] qui est à moitié au dessus de 1.
S = 0.5 - AUC # surface entre la première bissectrice et le courbe de Lorenz
gini = 2*S
print('Gini :', gini)'''


# J'analyse la corrélation entre 2 variables quantitatives
depenses = data[data.montant < 0]
plt.plot(depenses['solde_avt_ope'], -depenses['montant'], 'o')
plt.xlabel('solde avant opération')
plt.ylabel('montant de dépense')
plt.show()


# Agréger le solde avant opération en différentes classes
taille_classe = 500 # taille des classes pour la discrétisation
groupes = [] # va recevoir les données agrégées à afficher
# on calcule des tranches allant de 0 au solde maximum par paliers de taille taille_classe
tranches = np.arange(0, max(depenses["solde_avt_ope"]), taille_classe)
tranches += taille_classe/2 # on décale les tranches d'une demi taille de classe
indices = np.digitize(depenses["solde_avt_ope"], tranches) # associe chaque solde à son numéro de classe

for ind, tr in enumerate(tranches):  # pour chaque tranche, ind reçoit le numéro de tranche et tr la tranche en question
    montants = -depenses.loc[indices == ind, "montant"]  # sélection des individus de la tranche ind
    if len(montants) > 0:
        g = {
            'valeurs': montants,
            'centre_classe': tr - (taille_classe / 2),
            'taille': len(montants),
            'quartiles': [np.percentile(montants, p) for p in [25, 50, 75]]
        }
        groupes.append(g)

plt.figure(figsize=(10, 7))

# affichage des boxplots
plt.boxplot([g["valeurs"] for g in groupes],
            positions=[g["centre_classe"] for g in groupes],  # abscisses des boxplots
            showfliers=False,  # on ne prend pas en compte les outliers
            widths=taille_classe * 0.7)  # largeur graphique des boxplots

# affichage des effectifs de chaque classe
for g in groupes:
    plt.text(g["centre_classe"], 0, "(n={})".format(g["taille"]), horizontalalignment='center', verticalalignment='top')
plt.show()

# Calculer le coefficient de Pearson et la covariance
print(st.pearsonr(depenses["solde_avt_ope"],-depenses["montant"])[0])
print(np.cov(depenses["solde_avt_ope"],-depenses["montant"],ddof=0)[1,0])
