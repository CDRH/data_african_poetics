import json
import re
import omeka
from datetime import datetime
from bs4 import BeautifulSoup

def build_people_dict(row, existing_item):
    #in the news people only
    try:
        built_item = existing_item if existing_item else {}
        #new_item['schema:name'][0]['@value'] = "value" is how you update
        #TODO need to separate out Index and In the News more
        update_item_value(built_item, "dcterms:title", row["Name Built"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        update_item_value(built_item, "dcterms:description", row["Biography"])
        update_item_value(built_item, "foaf:givenName", row["Name given"])
        update_item_value(built_item, "foaf:lastName", row["Name last"])
        try:
            #make sure date can be parsed in the correct format, will throw exception if not
            date = datetime.strptime(row["Date birth"], '%Y-%m-%d')
            if date:
                update_item_value(built_item, "dcterms:date", row["Date birth"])
        except:
            print(row["Date birth"] + " is not a valid date")
            pass
        update_item_value(built_item, "dcterms:bibliographicCitation", row["Bio Sources (MLA)"])
        update_item_value(built_item, "dcterms:spatial", location(row["birth_spatial.city"]))
        update_item_value(built_item, "dcterms:coverage", location(row["nationality-region"]))
        names = get_matching_names_from_markdown(row, "related-people")
        if names:
            update_item_value(built_item, "dcterms:relation", names)
        lat = json.loads(row["Latitude (from Place of birth)"])[0]
        lon = json.loads(row["Longitude (from Place of birth)"])[0]
        if lat and lon:
            update_item_value(built_item, "geo:lat_long", f"{lat}, {lon}")
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
        update_item_value(built_item, "dcterms:title", row["Name"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        content = re.sub('<[^<]+?>', '', row["Content"])
        update_item_value(built_item, "dcterms:description", content)
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
        names = get_matching_names_from_markdown(row, "person-poet")
        if names:
            update_item_value(built_item, "dcterms:subject", names)
        citation = row["Works Cited"]
        update_item_value(built_item, "dcterms:bibliographicCitation", BeautifulSoup(citation, 'html.parser').get_text())
        return built_item
    except ValueError:
        breakpoint()

def build_events_dict(row, existing_item):
    #i'm not sure it makes sense to combine this in one method, but creating and updating are different processes
    try:
        built_item = existing_item if existing_item else {}
        update_item_value(built_item, "dcterms:title", row["Name"])
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        try:
            #make sure date can be parsed in the correct format, will throw exception if not
            date = datetime.strptime(row["Date"], '%Y-%m-%d')
            if date:
                update_item_value(built_item, "dcterms:date", row["Date"])
        except:
            print(row["Date"] + " is not a valid date")
            pass
        update_item_value(built_item, "dcterms:description", row["Summary"])
        names = get_matching_names_from_markdown(row, "person-poet")
        if names:
            update_item_value(built_item, "dcterms:references", names)
        if row["Latitude (from [location])"] and row["Longitude (from [location])"]:
            lat = json.loads(row["Latitude (from [location])"])[0]
            lon = json.loads(row["Longitude (from [location])"])[0]
            if lat and lon:
                update_item_value(built_item, "geo:lat", lat)
                update_item_value(built_item, "geo:long", lon)
        return built_item
    except ValueError:
        breakpoint()

def build_news_items_dict(row, existing_item):
    try:
        built_item = existing_item if existing_item else {}
        update_item_value(built_item, "dcterms:title", row["Article title"])
        # change if we move away from CDRH IDs
        update_item_value(built_item, "dcterms:identifier", row["Unique ID"])
        #format date properly, should be in yyyy-mm-dd format
        try:
            #make sure date can be parsed in the correct format, will throw exception if not
            date = datetime.strptime(row["Article Date (formatted)"], '%Y-%m-%d')
            if date:
                update_item_value(built_item, "dcterms:date", row["Article Date (formatted)"])
        except:
            print(row["Article Date (formatted)"] + " is not a valid date")
            pass
        update_item_value(built_item, "dcterms:description", row["Excerpt"])
        update_item_value(built_item, "dcterms:bibliographicCitation", build_citation(row))
        #this one already works, I am filtering for names without ids
        names = get_matching_names_from_markdown(row, "person")
        if names:
            update_item_value(built_item, "dcterms:references", names)
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
        #format date properly, should be in yyyy format
        try:
            date = datetime.strptime(row["Year"], '%Y')
            update_item_value(built_item, "dcterms:created", date)
        except:
            print(row["Year"] + " is not a valid date")
            pass
        if row["publisher"]:
            update_item_value(built_item, "dcterms:publisher", json.loads(row["publisher"]))
        #determine airtable column and how it should be parsed (if it's one of the md columns)
        names = get_matching_names_from_markdown(row, "person")
        if names:
            update_item_value(built_item, "dcterms:references", names)
        return built_item
    except ValueError:
        breakpoint()

def create_tags(tag):
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
    if row["Poet Omeka ID (Index of Poets)"]:
         link_item_record(existing_item, "dcterms:references", row["Poet Omeka ID (Index of Poets)"], filter_property="o:id")
    if row["University Omeka ID"]:
        link_item_record(existing_item, "foaf:maker", json.loads(row["University Omeka ID"]), filter_property="o:id")
    if row["Place of Birth Omeka ID"]:
        #look up place name
        link_item_record(existing_item, "geo:location", json.loads(row["Place of Birth Omeka ID"]), filter_property="o:id")
    item_set_id = get_ids_from_tags("[\"Poets in the News\"]")
    existing_item["o:item_set"] = item_set_id
    link_item_record(existing_item, "dcterms:type", item_set_id, item_set=True)
    return existing_item
    # need to get matching item TODO add conditional logic for blank entries
    # update_item_value(built_item, "foaf:maker", row["University Omeka ID (from [universities]) (from educations [join])"])

def link_commentaries(row, existing_item):
    cdrh_news_ids = get_matching_ids_from_markdown(row, "news-items_medium")
    if cdrh_news_ids:
        link_item_record(existing_item, "bibo:cites", cdrh_news_ids)
    cdrh_person_ids = get_matching_ids_from_markdown(row, "person-poet")
    if cdrh_person_ids:
        link_item_record(existing_item, "dcterms:subject", cdrh_person_ids)
    cdrh_event_ids = get_matching_ids_from_markdown(row, "events-subjects")
    if cdrh_event_ids:
        link_item_record(existing_item, "dcterms:references", cdrh_event_ids)
    cdrh_work_ids = get_matching_ids_from_markdown(row, "works")
    if cdrh_work_ids:
        link_item_record(existing_item, "dcterms:relation", cdrh_work_ids)
    item_set_id = get_ids_from_tags("[\"Commentary\"]")
    existing_item["o:item_set"] = item_set_id
    link_item_record(existing_item, "dcterms:type", item_set_id, item_set=True)
    return existing_item

def link_news_items(row, existing_item):
    if row["creator.name"]:
        #look up creator name by title
        link_item_record(existing_item, "dcterms:creator", json.loads(row["creator.name"]), filter_property="dcterms:title")
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
    if row["Publication Internal ID"]:
        publisher_ids = json.loads(row["Publication Internal ID"])
        if publisher_ids:
            link_item_record(existing_item, "dcterms:publisher", publisher_ids)
    tag_ids = get_ids_from_tags(row["Tags"])
    if tag_ids:
        existing_item["o:item_set"] = tag_ids
        link_item_record(existing_item,"dcterms:subject", tag_ids, item_set=True)
    item_set_id = get_ids_from_tags("[\"News Items\"]")
    existing_item["o:item_set"].append(item_set_id[0])
    link_item_record(existing_item, "dcterms:type", item_set_id, item_set=True)
    return existing_item
    #TODO add code to handle blank entries
    #TODO works are also here, but I don't think there is a field/Airtable column at present

def link_events(row, existing_item):
    if row["spatial.country"]:
        #look up country by title
        country = json.loads(row["spatial.country"])
        link_item_record(existing_item, "dcterms:spatial", country, filter_property="dcterms:title")
        if row["spatial.city"]:
            #look up county, city by title
            city = json.loads(row["spatial.country"])[0] + ", " + json.loads(row["spatial.city"])[0]
            link_item_record(existing_item, "geo:location", [city], filter_property="dcterms:title")
    if row["spatial.place"]:
        #look up place name
        link_item_record(existing_item, "foaf:based_near", json.loads(row["spatial.place"]), filter_property="foaf:based_near")
    # update_item_value(built_item, "foaf:based_near", row["places"])
    # update_item_value(built_item, "dcterms:spatial", location(row["spatial.country"]))
    cdrh_news_ids = get_matching_ids_from_markdown(row, "news_items")
    if cdrh_news_ids:
        link_item_record(existing_item, "dcterms:isReferencedBy", cdrh_news_ids)
    cdrh_person_ids = get_matching_ids_from_markdown(row, "person-poet")
    if cdrh_person_ids:
        link_item_record(existing_item, "dcterms:references", cdrh_person_ids)
    cdrh_commentary_ids = get_matching_ids_from_markdown(row, "commentaries_relation")
    if cdrh_commentary_ids:
        link_item_record(existing_item, "foaf:depiction", cdrh_commentary_ids)
    item_set_id = get_ids_from_tags("[\"Event\"]")
    existing_item["o:item_set"] = item_set_id
    link_item_record(existing_item, "dcterms:type", item_set_id, item_set=True)
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
    item_set_id = get_ids_from_tags("[\"Works\"]")
    existing_item["o:item_set"] = item_set_id
    link_item_record(existing_item, "dcterms:type", item_set_id, item_set=True)
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
        # make sure values are unique
        value = list(set(value))
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
    return item



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
                if name_match and not id_match.group(1):
                    name = name_match.group(1)
                    names.append(name)
            else:
                for value in markdown_values:
                    #parse with regex to get ids
                    # ruby code below
                    # /\]\((.*)\)/.match(query)[1] if /\]\((.*)\)/.match(query)
                    name_match = re.search(r"\[(.*?)\]", value)
                    id_match = re.search(r"\]\((.*)\)", value)
                    if name_match and not id_match.group(1):
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
        item_sets = omeka.item_sets()
        # TODO refactor so that API isn't called over and over again

        for tag in parsed_tags:
            matching_items = [s for s in item_sets if s["dcterms:title"][0]["@value"] == tag]
            if matching_items:
                ids.append(matching_items[0]["o:id"])
    return ids
            

def get_omeka_ids(lookup_values, filter_property):
    #lookup_values are usually a list of cdrh_ids, but may be another value
    omeka_ids = []
    for lookup_value in lookup_values:
        if lookup_value == '':
            continue
        if filter_property == "o:id":
            omeka_ids.append(int(lookup_value))
        else:
            match = omeka.omeka.filter_items_by_property(filter_property = filter_property, filter_value = lookup_value)
            if match["total_results"] >= 1:
                if match["total_results"] > 1:
                    print(f"warning: multiple matches for {lookup_value}, taking first match")
                omeka_id = match['results'][0]["o:id"]
                omeka_ids.append(omeka_id)
            else:
                print(f"Unable to link {lookup_value}, no matches")
    return omeka_ids



def link_item_record(item, key, values, item_set=False, filter_property = "dcterms:identifier"):
    omeka_ids = values if item_set else get_omeka_ids(values, filter_property)
    #dedupe
    omeka_ids = list(set(omeka_ids))
    prop_id = omeka.omeka.get_property_id(key)
    if not key in item:
        item[key] = []
    # if there are no ids found, just add the provided value(s) under the provided key
    if len(omeka_ids) == 0:
        for value in values:
            prop_value = {
                "value": value
            }
            formatted = omeka.omeka.prepare_property_value(prop_value, prop_id)
            item[key].append(formatted)

    resource_type = "resource:itemset" if item_set else "resource:item"
    for omeka_id in omeka_ids:
        #make sure item isn't already linked, to avoid duplicates
        if not item[key] or not omeka_id in [value.get("value_resource_id") for value in item[key]]:
            prop_value = {
                "type": resource_type,
                "value": omeka_id
            }
            formatted = omeka.omeka.prepare_property_value(prop_value, prop_id)
            #different format for item sets, plugin doesn't do it automatically
            if item_set:
                formatted['@id'] = f'{omeka.omeka_auth.api_url}/item_sets/{omeka_id}'
                formatted['value_resource_id'] = omeka_id
                formatted["value_resource_name"] = "item_sets"
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
            "{row["title"]}", {json.loads(row["publisher"])[0]}, {row["Article Date (formatted)"]}, {row["Source page no"]}.
            Accessed {row["Source access date"]}. {row["Source link"]}.
        """
