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
omeka = OmekaAPIClient('http://libr-cdrh2102vs3.unl.edu/omeka-s/api')
omeka_auth = OmekaAPIClient(
    api_url = 'http://libr-cdrh2102vs3.unl.edu/omeka-s/api',
    key_identity=os.getenv('KEY_IDENTITY'),                        
    key_credential=os.getenv('KEY_CREDENTIAL')                        
)
print(omeka_auth.get_template_properties(1))
#
tables = [
    "people",
    "commentaries",
    "events",
    "news items",
    "works"
]
#iterate through tables
#load tables, note that I am just starting with one at first
for table in tables:
    with open(f'source/csv/{table}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            #check if item is in index already
            matching_items = omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["Unique ID"])
            if matching_items:
                #if item exists, update item
                if matching_items["total_results"] == 1:
                    item_to_update = copy.deepcopy(matching_items["results"][0])
                    updated_item = api_fields.prepare_item(row, table, item_to_update)
                    if updated_item:
                        omeka_auth.update_resource(updated_item, "items")
                #otherwise, create item from scratch
                elif matching_items["total_results"] == 0:
                    new_item = api_fields.prepare_item(row, table)
                    payload = omeka_auth.prepare_item_payload_using_template(new_item, 1)
                    if payload:
                        omeka_auth.add_item(payload)
                #if multiple matches
                else:
                    print(f"multiple matches for {row['Unique ID']}, please check Omeka admin site")
        else:
            break
