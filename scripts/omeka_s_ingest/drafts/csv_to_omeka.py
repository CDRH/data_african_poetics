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
    with open('source/csv/#{table}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            #prepare item
            item = api_fields.prepare_item(row, table)
            # payload = omeka_auth.prepare_item_payload(item)
            payload = omeka_auth.prepare_item_payload_using_template(item, 1)
            #add item
            breakpoint()
            new_item = omeka_auth.add_item(payload)
