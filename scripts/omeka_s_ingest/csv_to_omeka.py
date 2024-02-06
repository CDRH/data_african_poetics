#import necessary modules, including csv and omeka, and the fields
import csv
import os
from omeka_s_tools.api import OmekaAPIClient


#initialize api and auth info
omeka = OmekaAPIClient('https://libr-cdrh2102vs3.unl.edu/omeka-s/api')
omeka_auth = OmekaAPIClient(
    api_url = 'https://libr-cdrh2102vs3.unl.edu/omeka-s/api',
    key_identity=os.getenv('KEY_IDENTITY'),                        
    key_credential=os.getenv('KEY_CREDENTIAL')                        
)
print(omeka_auth.get_template_properties(1))
#iterate through tables
#load tables, note that I am just starting with one at first
with open('source/csv/people.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row)
        #prepare item
        item = prepare_item(row)
        # payload = omeka_auth.prepare_item_payload(item)
        payload = omeka_auth.prepare_item_payload_using_template(item, 1)
        #add item
        new_item = omeka_auth.add_item(payload)
