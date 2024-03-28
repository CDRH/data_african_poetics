import json
import re
import omeka
import math

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
        update_item_value(built_item, "foaf:maker", education(row["year_degree_institution"]))
        update_item_value(built_item, "dcterms:type", "Person")
        update_item_value(built_item, "geo:location", location(row["birth_spatial.country"]))
        update_item_value(built_item, "dcterms:spatial", location(row["birth_spatial.city"]))
        update_item_value(built_item, "foaf:based_near", location(row["nationality-region"]))
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
        #update_item_value(built_item, "dcterms:references", row["Poet Omeka ID (Index of Poets)"])
        update_item_value(built_item, "foaf:givenName", row["Name given"])
        update_item_value(built_item, "foaf:lastName", row["Name last"])
        update_item_value(built_item, "foaf:gender", row["Gender"])
        #update_item_value(built_item, "dcterms:bibliographicCitation", row["Bio Sources (MLA)"])
        # TODO there needs to be conditional logic here to deal with blank entries and make them 
        # update_item_value(built_item, "foaf:maker", row["University Omeka ID (from [universities]) (from educations [join])"])
        # update_item_value(built_item, "foaf:isPrimaryTopicOf", row["News Item Omeka ID (from news item role join table)"])
        # update_item_value(built_item, "dcterms:isReferencedBy", row["Event Omega ID (from events table)"])
        # update_item_value(built_item, "foaf:made", row["Work Omega ID (from works table)"])
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
        if row["creator.name"]:
            update_item_value(built_item, "dcterms:creator", json.loads(row["creator.name"]))
        # TODO below fields need some conditional logic for blank entries

        # TODO below fields are waiting on an airtable column
        # update_item_value(built_item, "dcterms:bibliographicCitation", "")
        # update_item_value(built_item, "dcterms:date", "")
        # update_item_value(built_item, "dcterms:language", "")
        # update_item_value(built_item, "dcterms:created", "")
        # I wonder if works should go into the below field
        #update_item_value(built_item, "dcterms:relation", get_json_value(row, "commentaries_relation"))
        update_item_value(built_item, "dcterms:type", "Commentary")
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
        #update_item_value(built_item, "dcterms:alternative", row["name-letter"])
        update_item_value(built_item, "foaf:based_near", row["places"])
        update_item_value(built_item, "dcterms:spatial", location(row["spatial.country"]))
        update_item_value(built_item, "dcterms:type", "Event")
        #TODO add code to handle blank entries

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
        if row["Tags"]:
            update_item_value(built_item, "dcterms:subject", json.loads(row["Tags"]))
        update_item_value(built_item, "dcterms:bibliographicCitation", build_citation(row))
        names = get_matching_names_from_markdown(row, "person")
        if names:
            update_item_value(built_item, "foaf:topic", names)
        return built_item
    except ValueError:
        breakpoint()

def build_works_dict(row, existing_item):
    try:
        built_item = existing_item if existing_item else {}
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:title", row["Title"])
        if row["person-author"]:
            update_item_value(built_item, "dcterms:creator", json.loads(row["person-author"]))
        update_item_value(built_item, "dcterms:created", row["Year"])
        if row["publisher"]:
            update_item_value(built_item, "dcterms:publisher", json.loads(row["publisher"]))
        update_item_value(built_item, "dcterms:type", "Works")
        #TODO check whether this column is correct. also need to include [news_items]
        update_item_value(built_item, "dcterms:isReferencedBy", row["[commentaries]"])
        #determine airtable column and how it should be parsed (if it's one of the md columns)
        update_item_value(built_item, "dcterms:references", row["References"])
        return built_item
    except ValueError:
        breakpoint()

def get_matching_tags(tag):
    built_tag = {}
    update_item_value(built_tag, "dcterms:title", tag)
    update_item_value(built_tag, "dcterms:description", f"A collection of news items related to {tag}.")
    return built_tag

def link_people(row, existing_item):
    cdrh_news_ids = get_matching_ids_from_markdown(row, "news item roles")
    if cdrh_news_ids:
        link_item_record(existing_item, "foaf:isPrimaryTopicOf", cdrh_news_ids)
    cdrh_event_ids = get_matching_ids_from_markdown(row, "events")
    if cdrh_event_ids:
        link_item_record(existing_item, "dcterms:isReferencedBy", cdrh_event_ids)
    cdrh_work_ids = get_matching_ids_from_markdown(row, "work roles")
    if cdrh_work_ids:
        link_item_record(existing_item, "foaf:made", cdrh_work_ids)
    cdrh_person_ids = get_matching_ids_from_markdown(row, "related-people")
    if cdrh_person_ids:
        link_item_record(existing_item, "dcterms:relation", cdrh_person_ids)
    cdrh_commentary_ids = get_matching_ids_from_markdown(row, "commentaries_relation")
    if cdrh_commentary_ids:
        link_item_record(existing_item, "foaf:depiction", cdrh_commentary_ids)
    return existing_item
    # need to get matching item TODO add conditional logic for blank entries
    # update_item_value(built_item, "foaf:maker", row["University Omeka ID (from [universities]) (from educations [join])"])

def link_commentaries(row, existing_item):
    cdrh_news_ids = get_matching_ids_from_markdown(row, "news-items_medium")
    if cdrh_news_ids:
        link_item_record(existing_item, "bibo_cites", cdrh_news_ids)
    cdrh_person_ids = get_matching_ids_from_markdown(row, "person-poet")
    if cdrh_person_ids:
        link_item_record(existing_item, "dcterms:subject", cdrh_person_ids)
    cdrh_event_ids = get_matching_ids_from_markdown(row, "events-subjects")
    if cdrh_event_ids:
        link_item_record(existing_item, "dcterms:references", cdrh_event_ids)
    cdrh_work_ids = get_matching_ids_from_markdown(row, "works")
    if cdrh_work_ids:
        link_item_record(existing_item, "dcterms:relation", cdrh_work_ids)
    return existing_item

def link_news_items(row, existing_item):
    cdrh_person_ids = get_matching_ids_from_markdown(row, "person")
    if cdrh_person_ids:
        link_item_record(existing_item, "dcterms:references", cdrh_person_ids)
    cdrh_event_ids = get_matching_ids_from_markdown(row, "subjects")
    if cdrh_event_ids:
        link_item_record(existing_item, "dcterms:relation", cdrh_event_ids)
    cdrh_work_ids = get_matching_ids_from_markdown(row, "works")
    if cdrh_work_ids:
        link_item_record(existing_item, "foaf:depicts", cdrh_work_ids)
    cdrh_commentary_ids = get_matching_ids_from_markdown(row, "commentaries_relation")
    if cdrh_commentary_ids:
        link_item_record(existing_item, "foaf:depiction", cdrh_commentary_ids)
    tag_ids = get_ids_from_tags(row["Tags"])
    if tag_ids:
        existing_item["o:item_set"] = tag_ids
    return existing_item
    #TODO add code to handle blank entries
    #TODO works are also here, but I don't think there is a field/Airtable column at present

def link_events(row, existing_item):
    cdrh_news_ids = get_matching_ids_from_markdown(row, "news_items")
    if cdrh_news_ids:
        link_item_record(existing_item, "dcterms:isReferencedBy", cdrh_news_ids)
    cdrh_person_ids = get_matching_ids_from_markdown(row, "person-poet")
    if cdrh_person_ids:
        link_item_record(existing_item, "dcterms:references", cdrh_person_ids)
    cdrh_commentary_ids = get_matching_ids_from_markdown(row, "commentaries_relation")
    if cdrh_commentary_ids:
        link_item_record(existing_item, "foaf:depiction", cdrh_commentary_ids)
    return existing_item

def link_works(row, existing_item):
    cdrh_person_ids = get_matching_ids_from_markdown(row, "person")
    if cdrh_person_ids:
        link_item_record(existing_item, "dcterms:references", cdrh_person_ids)
    cdrh_news_ids = get_matching_ids_from_markdown(row, "news_items")
    if cdrh_news_ids:
        link_item_record(existing_item, "dcterms:isReferencedBy", cdrh_news_ids)
    cdrh_commentary_ids = get_matching_ids_from_markdown(row, "commentaries_relation")
    if cdrh_commentary_ids:
        link_item_record(existing_item, "foaf:depiction", cdrh_commentary_ids)
    # TODO need to add commentaries
    return existing_item

# def spatial(row):
#     places = []
#     if row["nationality-region"]:
#         places.append({ "region" : json.loads(row["nationality-region"])[0], "type": "nationality" })
#     if row["birth_spatial.country"]:
#       birthplace = { "country" : json.loads(row["birth_spatial.country"])[0], "type": "birth place" }
#       if row["birth_spatial.city"]:
#         birthplace["city"] = json.loads(row["birth_spatial.city"])[0]
#       places.append(birthplace)
#     return places


def prepare_item(row, table, existing_item = None):
    if table == "people" and "In the News" in row["site section"]:
        item_dict = build_people_dict(row, existing_item)
    elif table == "people" and "Index of Poets" in row["site section"]:
        # skipping for now
        #item_dict = build_people_index_dict(row, existing_item)
        print("Index of Poets ingest not implemented yet")
        return None
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

def link_records(row, table, existing_item):
    if table == "people":
        item_dict = link_people(row, existing_item)
    elif table == "commentaries":
        item_dict = link_commentaries(row, existing_item)
    elif table == "events":
        item_dict = link_events(row, existing_item)
    elif table == "news items":
        item_dict = link_news_items(row, existing_item)
    elif table == "works":
        item_dict = link_works(row, existing_item)
    else:
        print(f"linking records for table {table} not yet implemented")
        return None
    return item_dict

def get_json_value(row, name):
    if len(row[name]) > 0:
        if row[name].startswith('["'):
            return json.loads(row[name])
        elif ";;;" in row[name]:
            return row[name].split(";;;")
        else:
            return row[name]
    else:
        return row[name]
    
def update_item_value(item, key, value):
    if type(value) == str:
        if key in item:
            item[key][0]['@value'] = value
        else: 
            #add the key
            item[key] = [ 
                {
                    "value": value
                }
            ]
    elif type(value) == list:
        if key not in item:
            item[key] = []
            for v in value:
                item[key].append(
                    { 
                        "value": v 
                    }
                )
        else:
            for i, v in enumerate(value):
                # replace value at the given index, if it exists
                try:
                    item[key][i]['@value'] = v
                # otherwise, prepare value and append it
                except IndexError:
                    prop_id = omeka.omeka.get_property_id(key)
                    prop_value = {
                        "value": v
                    }
                    formatted = omeka.omeka.prepare_property_value(prop_value, prop_id)
                    item[key].append(formatted)



def get_matching_ids_from_markdown(row, field):
    # takes in an array of strings in markdown format, which include CDRH IDs
    # returns an array of just the IDs
    if row[field]:
        markdown_values = get_json_value(row, field)
        ids = []

        if markdown_values:
            #should be either single value or array
            if type(markdown_values) == str:
                match = re.search(r"\]\((.*)\)", markdown_values)
                if match:
                    id_no = match.group(1)
                    ids.append(id_no)
            else:
                for value in markdown_values:
                    #parse with regex to get ids
                    # ruby code below
                    # /\]\((.*)\)/.match(query)[1] if /\]\((.*)\)/.match(query)
                    match = re.search(r"\]\((.*)\)", value)
                    if match:
                        id_no = match.group(1)
                        ids.append(id_no)
                if len(ids) > 1:
                    ids = list(filter(None, ids))
            return ids
            
    else:
        return []
    
def get_matching_names_from_markdown(row, field):
    # takes in an array of strings in markdown format, which include names
    # returns an array of just the names
    # filters out the ones that have a corresponding id, it is not necessary to get their names
    if row[field]:
        markdown_values = get_json_value(row, field)
        names = []

        if markdown_values:
            #should be either single value or array
            if type(markdown_values) == str:
                name_match = re.search(r"\[(.*?)\]", markdown_values)
                # filter out entries that have ids
                id_match = re.search(r"\]\((.*)\)", markdown_values)
                if name_match and not id_match:
                    name = name_match.group(1)
                    names.append(name)
            else:
                for value in markdown_values:
                    #parse with regex to get ids
                    # ruby code below
                    # /\]\((.*)\)/.match(query)[1] if /\]\((.*)\)/.match(query)
                    name_match = re.search(r"\[(.*?)\]", value)
                    id_match = re.search(r"\]\((.*)\)", value)
                    if name_match and not id_match:
                        name = name_match.group(1)
                        names.append(name)
            return names
    else:
        return []
    
def get_ids_from_tags(tags):
    #given the name, find id of the resource template
    ids = []
    if tags:
        parsed_tags = json.loads(tags)
        #get all item sets so we can sort through them
        # below looks simple, but will not work because only returns the first page of results
        # item_sets = omeka.omeka.get_resources("item_sets")["results"]
        item_sets = []
        # TODO refactor so that API isn't called over and over again
        pages = math.ceil(omeka.omeka.get_resources("item_sets")["total_results"] / 5)
        for i in range(pages):
            item_sets += omeka.omeka.get_resources("item_sets", page=i)["results"]
        for tag in parsed_tags:
            matching_items = [s for s in item_sets if s["dcterms:title"][0]["@value"] == tag]
            if matching_items:
                ids.append(matching_items[0]["o:id"])
    return ids
            

def get_omeka_ids(cdrh_ids):
    omeka_ids = []
    for cdrh_id in cdrh_ids:
        if cdrh_id == '':
            continue
        match = omeka.omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = cdrh_id)
        if match["total_results"] == 1:
            omeka_id = match['results'][0]["o:id"]
            omeka_ids.append(omeka_id)
        else:
            print(match)
            print(f"Unable to link {cdrh_id}, match not found or multiple matches")
    return omeka_ids

def link_item_record(item, key, cdrh_ids):
    omeka_ids = get_omeka_ids(cdrh_ids)
    prop_id = omeka.omeka.get_property_id(key)
    item[key] = []
    for omeka_id in omeka_ids:
        prop_value = {
            "type": "resource:item",
            "value": omeka_id
        }
        formatted = omeka.omeka.prepare_property_value(prop_value, prop_id)
        item[key].append(formatted)
    return item

def education(markdown):
    if markdown and len(markdown) > 0:
        educations = []
        for school in json.loads(markdown):
            educations.append(school.split(":")[1].strip())
        return educations

def location(markdown):
    if markdown and len(markdown) > 0:
        return json.loads(markdown)[0]
    
def build_citation(row):
    # TODO format the date better
    if row["publisher"]:
        return f"""
            "{row["title"]}", {row["publisher"][0]}, {row["Article Date (formatted)"]}, {row["Source page no"]}.
            Accessed {row["Source access date"]}. {row["Source link"]}.
        """
