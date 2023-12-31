# Import des modules nécessaires
import pymongo  # Pour interagir avec MongoDB
import pandas as pd  # Manipulation des données avec des DataFrames
import matplotlib.pyplot as plt  # Création de graphiques
import utils  # Module personnalisé contenant des fonctions utilitaires
from constant import (
    DB_URL,
)  # Import de l'URL de la base de données depuis un fichier constant

# Connexion à la base de données MongoDB
client = pymongo.MongoClient(
    DB_URL
)  # Établissement d'une connexion avec MongoDB via l'URL fournie
db = client["tourism"]  # Accès à la base de données "tourism"
collection = db["logement"]  # Accès à la collection "logement" dans la base de données

# Spécification des champs pour le regroupement des données
group_by = {"Pays": "$Pays", "Mois": "$Mois", "Année": "$Année"}
value_field = "Valeur"  # Champ utilisé pour les calculs statistiques
calculations = [
    "Somme",
    "Moyenne",
    "Maximum",
    "Minimum",
]  # Types de calculs à effectuer

# Création du pipeline d'agrégation MongoDB à l'aide de fonctions utilitaires
pipeline = utils.create_aggregation_pipeline(
    group_by=group_by, value_field=value_field, calculations=calculations
)

# Exécution du pipeline pour obtenir les résultats de l'agrégation depuis la collection spécifiée
result_mongo = utils.execute_pipeline(pipeline=pipeline, collection=collection)

# Transformation des résultats obtenus depuis MongoDB en un DataFrame pandas
df = pd.DataFrame(list(result_mongo))

# Visualisation des données sous forme de graphiques

# Histogramme montrant l'analyse du logement par pays
df.plot(kind="hist", x="Pays", y="Somme", title="Analyse de logement par pays")

# Graphique en zone pour analyser le logement par mois par pays
df.plot(kind="area", x="Mois", y="Somme", title="Analyse de logement par Mois par Pays")

# Graphique en ligne pour analyser le logement par année par pays
df.plot(
    kind="line", x="Année", y="Somme", title="Analyse de logement par Année par Pays"
)

# Nuage de points pour représenter la valeur moyenne du logement par pays
df.plot(
    kind="scatter",
    y="Pays",
    x="Moyenne",
    title="Analyse de la valeur moyenne du logement par pays",
)
plt.xlabel("Pays")  # Label pour l'axe x
plt.ylabel("Logement")  # Label pour l'axe y
plt.show()  # Affichage des graphiques

# Export des données analysées vers un fichier CSV dans le répertoire de sortie spécifié
df.to_csv("./output/export.csv", index=False)
