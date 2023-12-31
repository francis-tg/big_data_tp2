import calendar
import locale

# Définir la locale en français
locale.setlocale(locale.LC_TIME, "en_EN.UTF-8")


def create_aggregation_pipeline(group_by, value_field, calculations):
    group_stage = {
        "$group": {
            "_id": {
                "Pays": f"{group_by['Pays']}",
                "Mois": f"{group_by['Mois']}",
                "Année": f"{group_by['Année']}",
            }
        }
    }

    project_stage = {
        "$project": {
            "_id": 0,
            "Pays": "$_id.Pays",
            "Mois": "$_id.Mois",
            "Année": "$_id.Année",
        }
    }

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

    pipeline = [group_stage, project_stage]
    return pipeline


def execute_pipeline(collection, pipeline: dict) -> list:  # exécute le le pipeline
    results = collection.aggregate(pipeline)
    return list(results)


def groupedData(data: list) -> list:
    # Map numerical month to month name
    months = {str(i): calendar.month_name[i] for i in range(1, 13)}
    grouped_data = []
    for entry in data:
        country = entry["GEO (Labels)"]
        del entry["GEO (Labels)"]  # Remove the country label from the entry
        for key, value in entry.items():
            year, month = key.split("-")
            month_name_fr = calendar.month_name[int(month)].capitalize()
            grouped_data.append(
                {"Pays": country, "Mois": month_name_fr, "Année": year, "Valeur": value}
            )
    return grouped_data


def removeUnamedToList(data, keyName="Unnamed") -> list:
    for entry in data:
        keys_to_remove = [key for key in entry.keys() if keyName in key]
        for key in keys_to_remove:
            del entry[key]
    return data
