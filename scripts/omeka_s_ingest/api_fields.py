import json

def build_people_dict(row, existing_item):
    #i'm not sure it makes sense to combine this in one method, but creating and updating are different processes
    try:
        built_item = existing_item if existing_item else {}
        #new_item['schema:name'][0]['@value'] = "value" is how you update
        update_item_value(built_item, "dcterms:title", row["Name Built"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:date", row["Date birth"])
        update_item_value(built_item, "dcterms:description", row["Biography"])
        update_item_value(built_item, "dcterms:spatial", spatial(row))
        update_item_value(built_item, "dcterms:alternative", row["name-letter"])
        update_item_value(built_item, "dcterms:format", get_json_value(row, "news item roles"))
        update_item_value(built_item, "dcterms:subject", get_json_value(row, "events"))
        update_item_value(built_item, "dcterms:relation", get_json_value(row, "commentaries_relation"))
        return built_item
    except ValueError:
        breakpoint()

def build_commentaries_dict(row, existing_item):
    #i'm not sure it makes sense to combine this in one method, but creating and updating are different processes
    try:
        built_item = existing_item if existing_item else {}
        #new_item['schema:name'][0]['@value'] = "value" is how you update
        update_item_value(built_item, "dcterms:type", "Commentaries")
        update_item_value(built_item, "dcterms:title", row["Name"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:description", row["Content"])
        update_item_value(built_item, "dcterms:format", row["news-items_medium"])
        update_item_value(built_item, "dcterms:subject", row["events-subjects"])
        update_item_value(built_item, "dcterms:creator", row["creator.name"])
        # I wonder if works should go into the below field
        #update_item_value(built_item, "dcterms:relation", get_json_value(row, "commentaries_relation"))
        return built_item
    except ValueError:
        breakpoint()

def build_events_dict(row, existing_item):
    #i'm not sure it makes sense to combine this in one method, but creating and updating are different processes
    try:
        built_item = existing_item if existing_item else {}
        #new_item['schema:name'][0]['@value'] = "value" is how you update
        update_item_value(built_item, "dcterms:title", row["Name Built"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:date", row["Date birth"])
        update_item_value(built_item, "dcterms:description", row["Biography"])
        update_item_value(built_item, "dcterms:temporal", row["topics-decade"])
        update_item_value(built_item, "dcterms:alternative", row["name-letter"])
        update_item_value(built_item, "dcterms:format", get_json_value(row, "news items"))
        update_item_value(built_item, "dcterms:relation", get_json_value(row, "commentaries_relation"))
        return built_item
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


def prepare_item(row, table, existing_item = None):
    if table == "people":
        item_dict = build_people_dict(row, existing_item)
    elif table == "commentaries":
        item_dict = build_commentaries_dict(row, existing_item)
    elif table == "events":
        item_dict = build_events_dict(row, existing_item)
    else:
        print(f"API for table {table} not yet implemented")
        return None
    return item_dict

def get_json_value(row, name):
    if len(row[name]) > 0:
        
        return json.loads(row[name])
    else:
        return row[name]
    
def update_item_value(item, key, value):
    if key in item:
        item[key][0]['@value'] = value
    else: 
        #add the key
        item[key] = [ 
            {
                "value": value
            }
        ]
