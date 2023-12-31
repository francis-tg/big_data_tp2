# Importation des modules nécessaires
import calendar  # Pour la manipulation des dates et des mois
import locale  # Pour la gestion des paramètres de localisation

# Définition de la locale en français
locale.setlocale(locale.LC_TIME, "en_EN.UTF-8")


# Fonction pour créer un pipeline d'agrégation MongoDB
def create_aggregation_pipeline(group_by, value_field, calculations):
    # Étape de groupage pour regrouper les données par Pays, Mois et Année
    group_stage = {
        "$group": {
            "_id": {
                "Pays": f"{group_by['Pays']}",
                "Mois": f"{group_by['Mois']}",
                "Année": f"{group_by['Année']}",
            }
        }
    }

    # Étape de projection pour formater les données
    project_stage = {
        "$project": {
            "_id": 0,
            "Pays": "$_id.Pays",
            "Mois": "$_id.Mois",
            "Année": "$_id.Année",
        }
    }

    # Boucle pour ajouter les opérations d'agrégation (Somme, Moyenne, Maximum, Minimum)
    for calc in calculations:
        if calc == "Somme":
            group_stage["$group"][calc] = {"$sum": f"${value_field}"}
            project_stage["$project"]["Somme"] = f"${calc}"
        elif calc == "Moyenne":
            group_stage["$group"][calc] = {"$avg": f"${value_field}"}
            project_stage["$project"]["Moyenne"] = f"${calc}"
        elif calc == "Maximum":
            group_stage["$group"][calc] = {"$max": f"${value_field}"}
            project_stage["$project"]["Maximum"] = f"${calc}"
        elif calc == "Minimum":
            group_stage["$group"][calc] = {"$min": f"${value_field}"}
            project_stage["$project"]["Minimum"] = f"${calc}"

    # Construction du pipeline d'agrégation final
    pipeline = [group_stage, project_stage]
    return pipeline


# Fonction pour exécuter un pipeline sur une collection MongoDB
def execute_pipeline(collection, pipeline: dict) -> list:
    results = collection.aggregate(pipeline)
    return list(results)


# Fonction pour formater les données pour l'insertion dans MongoDB
def groupedData(data: list) -> list:
    # Création d'une correspondance numérique -> nom du mois en français
    months = {str(i): calendar.month_name[i] for i in range(1, 13)}
    grouped_data = []
    # Transformation des données pour les adapter à l'insertion dans la base de données
    for entry in data:
        country = entry["GEO (Labels)"]
        del entry["GEO (Labels)"]  # Suppression du libellé du pays de l'entrée
        for key, value in entry.items():
            year, month = key.split("-")
            # Conversion du mois numérique en nom du mois en français
            month_name_fr = calendar.month_name[int(month)].capitalize()
            grouped_data.append(
                {"Pays": country, "Mois": month_name_fr, "Année": year, "Valeur": value}
            )
    return grouped_data


# Fonction pour supprimer les clés non nommées d'un dictionnaire
def removeUnamedToList(data, keyName="Unnamed") -> list:
    for entry in data:
        # Récupération des clés à supprimer basées sur le nom donné
        keys_to_remove = [key for key in entry.keys() if keyName in key]
        # Suppression des clés non nommées du dictionnaire
        for key in keys_to_remove:
            del entry[key]
    return data


""" 
Importation des modules : Importe les modules nécessaires pour gérer les dates, les mois et les paramètres de localisation.

Définition de la locale en français : Configure la locale pour afficher les mois en français.

Fonction create_aggregation_pipeline : Crée un pipeline d'agrégation MongoDB en fonction des spécifications de groupage, du champ de valeur et des calculs à réaliser.

Fonction execute_pipeline : Exécute un pipeline sur une collection MongoDB et retourne les résultats.

Fonction groupedData : Transforme les données en un format adapté pour l'insertion dans une base de données MongoDB, en convertissant les mois numériques en noms de mois en français et en organisant les données par pays, mois et année.

Fonction removeUnamedToList : Supprime les clés non nommées d'un dictionnaire, généralement utilisée pour nettoyer les données avant l'insertion dans une base de données.

Ces fonctions sont conçues pour faciliter la préparation des données avant leur insertion dans une base de données MongoDB, en les adaptant à la structure attendue pour les opérations d'agrégation et d'insertion.
"""
