import json
import re

def build_people_dict(row, existing_item):
    #in the news people only
    try:
        built_item = existing_item if existing_item else {}
        #new_item['schema:name'][0]['@value'] = "value" is how you update
        #TODO need to separate out Index and In the News more
        update_item_value(built_item, "dcterms:title", row["Name Built"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:description", row["Biography"])
        #update_item_value(built_item, "dcterms:spatial", spatial(row))
        #update_item_value(built_item, "dcterms:alternative", row["name-letter"])
        update_item_value(built_item, "dcterms:references", row["Poet Omeka ID (Index of Poets)"])
        update_item_value(built_item, "foaf:givenName", row["Name given"])
        update_item_value(built_item, "foaf:lastName", row["Name last"])
        update_item_value(built_item, "dcterms:bibliographicCitation", row["Bio Sources (MLA)"])
        
        return built_item
    except ValueError:
        breakpoint()

def build_people_index_dict(row, existing_item):
    #TODO haven't started implementing this
    try:
        built_item = existing_item if existing_item else {}
        #new_item['schema:name'][0]['@value'] = "value" is how you update
        #TODO need to separate out Index and In the News more
        update_item_value(built_item, "dcterms:title", row["Name Built"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "foaf:birthday", row["Date birth"])
        update_item_value(built_item, "dcterms:description", row["Biography"])
        #update_item_value(built_item, "dcterms:spatial", spatial(row))
        update_item_value(built_item, "dcterms:alternative", row["name-letter"])
        #update_item_value(built_item, "dcterms:format", get_json_value(row, "news item roles"))
        #update_item_value(built_item, "dcterms:subject", get_json_value(row, "events"))
        #update_item_value(built_item, "dcterms:relation", get_json_value(row, "commentaries_relation"))
        update_item_value(built_item, "dcterms:references", row["Poet Omeka ID (Index of Poets)"])
        update_item_value(built_item, "foaf:givenName", row["Name given"])
        update_item_value(built_item, "foaf:lastName", row["Name last"])
        update_item_value(built_item, "foaf:gender", row["Gender"])
        update_item_value(built_item, "dcterms:bibliographicCitation", row["Bio Sources (MLA)"])
        # TODO there needs to be conditional logic here to deal with blank entries
        update_item_value(built_item, "foaf:maker", row["University Omeka ID (from [universities]) (from educations [join])"])
        update_item_value(built_item, "foaf:isPrimaryTopicOf", row["News Item Omeka ID (from news item role join table)"])
        update_item_value(built_item, "dcterms:isReferencedBy", row["Event Omega ID (from events table)"])
        update_item_value(built_item, "foaf:made", row["Work Omega ID (from works table)"])
        # there is some more API magic to do here but that is TODO later. currently no value. 
        # update_item_value(built_item, "foaf:img", "")
        # these ones do not have an airtable column. TODO either wait on airtable column
        # or make functions to calculate the values
        # update_item_value(built_item, "foaf:status", "")
        # update_item_value(built_item, "dcterms:relation", "")
        
        return built_item
    except ValueError:
        breakpoint()

def build_commentaries_dict(row, existing_item):
    #i'm not sure it makes sense to combine this in one method, but creating and updating are different processes
    try:
        built_item = existing_item if existing_item else {}
        #new_item['schema:name'][0]['@value'] = "value" is how you update
        #update_item_value(built_item, "dcterms:type", "Commentaries")
        update_item_value(built_item, "dcterms:title", row["Name"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:description", row["Content"])
        #update_item_value(built_item, "dcterms:format", row["news-items_medium"])
        update_item_value(built_item, "dcterms:subject", row["events-subjects"])
        update_item_value(built_item, "dcterms:creator", row["creator.name"])
        # TODO below fields need some conditional logic for blank entries
        update_item_value(built_item, "dcterms:references", row["Events Omeka ID"])
        update_item_value(built_item, "bibo:cites", row["News Item Omeka ID"])
        update_item_value(built_item, "dcterms:subject", row["Referenced Poet Omeka ID"])
        update_item_value(built_item, "dcterms:relation", row["Works Omeka ID"])
        # TODO below fields are waiting on an airtable column
        # update_item_value(built_item, "dcterms:bibliographicCitation", "")
        # update_item_value(built_item, "dcterms:date", "")
        # update_item_value(built_item, "dcterms:language", "")
        # update_item_value(built_item, "dcterms:created", "")
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
        update_item_value(built_item, "dcterms:title", row["Name"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:date", row["Date"])
        update_item_value(built_item, "dcterms:description", row["Summary"])
        #update_item_value(built_item, "dcterms:temporal", row["topics-decade"])
        # update_item_value(built_item, "dcterms:alternative", row["name-letter"])
        update_item_value(built_item, "dcterms:spatial", row["Location (Country)"])
        update_item_value(built_item, "foaf:based_near", row["Location (City)"])
        update_item_value(built_item, "dcterms:type", row["Event type"])
        #TODO add code to handle blank entries
        update_item_value(built_item, "dcterms:isReferencedBy", row["Related News Item Omeka ID"])
        update_item_value(built_item, "dcterms:references", row["Related Poet Omeka ID"])

        #update_item_value(built_item, "dcterms:format", get_json_value(row, "news items"))
        #update_item_value(built_item, "dcterms:relation", get_json_value(row, "commentaries_relation"))
        return built_item
    except ValueError:
        breakpoint()

def build_news_items_dict(row, existing_item):
    try:
        built_item = existing_item if existing_item else {}
        update_item_value(built_item, "dcterms:title", row["Article title"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:creator", row["creator.name"])
        update_item_value(built_item, "dcterms:date", row["Article Date (formatted)"])
        update_item_value(built_item, "dcterms:publisher", row["[publication]"]) #TODO make sure this is a readable field
        update_item_value(built_item, "dcterms:description", row["Excerpt"])
        update_item_value(built_item, "dcterms:subject", row["Tags"])
        update_item_value(built_item, "dcterms:bibliographicCitation", row["Source link"])
        #TODO add code to handle blank entries
        update_item_value(built_item, "dcterms:relation", row["Related Event Omeka ID"])
        update_item_value(built_item, "dcterms:references", row["Contributor Omeka ID"])
        return built_item
    except ValueError:
        breakpoint()

def build_works_dict(row, existing_item):
    try:
        built_item = existing_item if existing_item else {}
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:title", row["Title"])
        update_item_value(built_item, "dcterms:creator", row["person-author"])
        update_item_value(built_item, "dcterms:created", row["Year"])
        update_item_value(built_item, "dcterms:publisher", row["publisher"])
        update_item_value(built_item, "dcterms:type", row["Work type"])
        #TODO check whether this column is correct. also need to include [news_items]
        update_item_value(built_item, "dcterms:isReferencedBy", row["[commentaries]"])
        #determine airtable column and how it should be parsed (if it's one of the md columns)
        update_item_value(built_item, "dcterms:references", row["References"])
        return built_item
    except ValueError:
        breakpoint()

def link_people(row, existing_item, omeka):

    cdrh_news_ids = get_matching_ids_from_markdown(row, "news item roles")
    link_item_record(existing_item, "foaf:isPrimaryTopicOf", omeka, cdrh_news_ids)
    return existing_item
    # need to get matching item TODO add conditional logic for blank entries
    # update_item_value(built_item, "foaf:maker", row["University Omeka ID (from [universities]) (from educations [join])"])
    # update_item_value(built_item, "foaf:isPrimaryTopicOf", row["News Item Omeka ID (from news item role join table)"])
    # update_item_value(built_item, "dcterms:isReferencedBy", row["Event Omega ID (from events table)"])
    # update_item_value(built_item, "foaf:made", row["Work Omega ID (from works table)"])


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
    elif table == "news items":
        item_dict = build_news_items_dict(row, existing_item)
    elif table == "works":
        item_dict = build_works_dict(row, existing_item)
    else:
        print(f"API for table {table} not yet implemented")
        return None
    return item_dict

def link_records(row, table, existing_item, omeka):
    if table == "people":
        item_dict = link_people(row, existing_item, omeka)
    # elif table == "commentaries":
    #     item_dict = build_commentaries_dict(row, existing_item)
    # elif table == "events":
    #     item_dict = build_events_dict(row, existing_item)
    # elif table == "news items":
    #     item_dict = build_news_items_dict(row, existing_item)
    # elif table == "works":
    #     item_dict = build_works_dict(row, existing_item)
    else:
        print(f"linking records for table {table} not yet implemented")
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

def get_matching_ids_from_markdown(row, field):
    # takes in an array of strings in markdown format, which include CDRH IDs
    # returns an array of just the IDs
    if row[field]:
        markdown_values = json.loads(row[field])

        ids = []
        for value in markdown_values:
            #parse with regex to get ids
            # ruby code below
            # /\]\((.*)\)/.match(query)[1] if /\]\((.*)\)/.match(query)
            match = re.search(r"\]\((.*)\)", value)
            if match:
                id_no = match.group(1)
                ids.append(id_no)
        return ids
    else:
        return []

def get_omeka_ids(cdrh_ids, omeka):
    omeka_ids = []
    for cdrh_id in cdrh_ids:
        match = omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = cdrh_id)
        if match["total_results"] == 1:
            omeka_id = match['results'][0]["o:id"]
            omeka_ids.append(omeka_id)
        else:
            print(match)
            print(f"Unable to link {cdrh_id}, match not found or multiple matches")
    return omeka_ids

def link_item_record(item, key, omeka, cdrh_ids):
    omeka_ids = get_omeka_ids(cdrh_ids, omeka)
    prop_id = omeka.get_property_id(key)
    item[key] = []
    for omeka_id in omeka_ids:
        prop_value = {
            "type": "resource:item",
            "value": omeka_id
        }
        formatted = omeka.prepare_property_value(prop_value, prop_id)
        item[key].append(formatted)
    return item