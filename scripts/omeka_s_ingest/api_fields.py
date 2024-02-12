import json

def build_people_dict(row):
    try:
        return {
            "dcterms:title": [
                {
                    "value": row["Name Built"]
                }
            ],
            "dcterms:identifier": [
                {
                    "value": row["Unique ID"]
                }
            ],
            "dcterms:date": [
                {
                    #note: standardized in the original
                    "value": row["Date birth"]
                }
            ],
            "dcterms:description": [
                {
                    "value": row["Biography"]
                }
            ],
            "dcterms:spatial": [
                {
                    "value": spatial(row)
                }
            ],
            "dcterms:alternative": [
                {
                    "value": row["name-letter"]
                }
            ],
            "dcterms:format": [
                {
                    "value": get_json_value(row, "news item roles")
                }
            ],
            "dcterms:subject": [
                {
                    "value": get_json_value(row, "events")
                }
            ],
            "dcterms:relation": [
                {
                    "value": get_json_value(row, "commentaries_relation")
                }
            ]
            
        }
    except ValueError:
        breakpoint()

def spatial(row):
    places = []
    if row["nationality-region"]:
        places.append({ "region" : json.loads(row["nationality-region"])[0], "type": "nationality" })

    if row["birth_spatial.country"]:
      birthplace = { "country" : json.loads(row["birth_spatial.country"])[0], "type": "birth place" }
      if row["birth_spatial.city"]:
        birthplace["city"] = json.loads(row["birth_spatial.city"])[0]

      places.append(birthplace)

    return places


def prepare_item(row, table):
    if table == "people":
        item_dict = build_people_dict(row)
    else:
        print(f"API for table {table} not yet implemented")
        return None
    return item_dict

def get_json_value(row, name):
    if len(row[name]) > 0:
        
        return json.loads(row[name])
    else:
        return row[name]
