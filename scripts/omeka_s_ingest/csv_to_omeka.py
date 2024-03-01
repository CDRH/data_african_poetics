#import necessary modules, including csv and omeka, and the fields
import csv
import os
from omeka_s_tools.api import OmekaAPIClient
import api_fields
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
import copy

#initialize api and auth info
#TODO can these be refactored as instance variables somehow?
omeka = OmekaAPIClient('http://libr-cdrh2102vs3.unl.edu/omeka-s/api')
omeka_auth = OmekaAPIClient(
    api_url = 'http://libr-cdrh2102vs3.unl.edu/omeka-s/api',
    key_identity=os.getenv('KEY_IDENTITY'),                        
    key_credential=os.getenv('KEY_CREDENTIAL')                        
)
tables = [
    "people",
    "commentaries",
    "events",
    "news items",
    "works"
]

def get_template_number_from_table(table):
    #return the number corresponding to the template for the type of item
    #ie news items, events, etc.
    match table:
        case "people":
            return 5
        case "commentaries":
            return 3
        case "events":
            return 4
        case "news items":
            return 6
        case "works":
            return 8


for table in tables:
    #iterate through each table in turn and read each csv row
    with open(f'source/csv/{table}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        template_number = get_template_number_from_table(table)
        # TODO eventually will need to have a way to split up index of poets and in the news
        for row in reader:
            # if posting the people table, check for items that should not be ingested
            if table == "people":
                if not (row["Completion Status"] == "Publish"  and
                        row["Manual data entry complete"] == "True" and
                        "In the News" in row["site section"] and 
                        row["Major african poet"] == "True"):
                    continue
            #check if item is in the API already TODO can this be made more efficient
            matching_items = omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["Unique ID"])
            if matching_items:
                #if item exists, update item
                if matching_items["total_results"] == 1:
                    print(f"updating item {matching_items["results"][0]["dcterms:identifier"][0]["@value"]}")
                    item_to_update = copy.deepcopy(matching_items["results"][0])
                    updated_item = api_fields.prepare_item(row, table, item_to_update)
                    if updated_item:
                        omeka_auth.update_resource(updated_item, "items")
                #otherwise, create item from scratch
                elif matching_items["total_results"] == 0:
                    print(f"creating item {row['Unique ID']}")
                    new_item = api_fields.prepare_item(row, table)
                    payload = omeka_auth.prepare_item_payload_using_template(new_item, template_number)
                    if payload:
                        omeka_auth.add_item(payload)
                #if multiple matches, warn but don't ingest
                else:
                    print(f"multiple matches for {row['Unique ID']}, please check Omeka admin site")
            else:
                break

#go through tables again to link records
for table in tables:
    #iterate through each table in turn and read each csv row
    with open(f'source/csv/{table}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # if posting the people table, check for items that should not be ingested
            if table == "people":
                if not (row["Completion Status"] == "Publish"  and
                        row["Manual data entry complete"] == "True" and
                        "In the News" in row["site section"] and 
                        row["Major african poet"] == "True"):
                    continue
            #check if item is in the API already TODO can this be made more efficient
            #everything should be in the API by now
            matching_items = omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["Unique ID"])
            if matching_items and matching_items["total_results"] == 1:
                #if item exists, update item with linked records
                print(f"linking records for {matching_items["results"][0]["dcterms:identifier"][0]["@value"]}")
                item_to_link = copy.deepcopy(matching_items["results"][0])
                linked_item = api_fields.link_records(row, table, item_to_link, omeka)
                if linked_item:
                    omeka_auth.update_resource(linked_item, "items")
                
            else:
                #if multiple matches or item not found, display warning
                print(f"error retrieving {row['Unique ID']}, please check Omeka admin site")
