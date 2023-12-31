# Importation des modules nécessaires
import pandas as pd  # Pour la manipulation des données avec des DataFrames
from pymongo import MongoClient  # Pour interagir avec MongoDB
from constant import (
    DB_URL,
)  # Import de l'URL de la base de données depuis un fichier constant
import utils  # Module personnalisé contenant des fonctions utilitaires

# Lecture des données Excel dans un DataFrame pandas à partir du fichier "traitement.xlsx"
df = pd.read_excel("./files/traitement.xlsx")

# Connexion à MongoDB en utilisant l'URL fournie dans le fichier de constantes
client = MongoClient(DB_URL)  # Établissement d'une connexion avec MongoDB via l'URL
db = client["tourism"]  # Accès à la base de données "tourism"
collection = db["logement"]  # Accès à la collection "logement" dans la base de données

# Conversion des données du DataFrame pandas en une liste de dictionnaires pour l'insertion dans MongoDB
listed_data: list = df.to_dict(orient="records")

# Utilisation de fonctions utilitaires pour préparer les données avant l'insertion dans la base de données
utils.removeUnamedToList(
    listed_data
)  # Suppression des clés non nommées dans les dictionnaires
grouped_data: list = utils.groupedData(
    listed_data
)  # Groupement des données pour l'insertion

# Insertion des données groupées dans la collection MongoDB
print(grouped_data)  # Affichage des données à insérer (pour le contrôle)
collection.insert_many(grouped_data)  # Insertion des données dans la collection MongoDB

# Exemple de pipeline MongoDB (commenté)
""" pipeline = [
    {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
    {"$sort": {"total": -1}},
    {"$limit": 5},
] """
