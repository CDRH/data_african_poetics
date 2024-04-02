import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
from omeka_s_tools.api import OmekaAPIClient
import math
omeka = OmekaAPIClient('http://libr-cdrh2102vs3.unl.edu/omeka-s/api')
omeka_auth = OmekaAPIClient(
    api_url = 'http://libr-cdrh2102vs3.unl.edu/omeka-s/api',
    key_identity=os.getenv('KEY_IDENTITY'),                        
    key_credential=os.getenv('KEY_CREDENTIAL')                        
)

def reset():
    omeka = OmekaAPIClient('http://libr-cdrh2102vs3.unl.edu/omeka-s/api')
    omeka_auth = OmekaAPIClient(
        api_url = 'http://libr-cdrh2102vs3.unl.edu/omeka-s/api',
        key_identity=os.getenv('KEY_IDENTITY'),                        
        key_credential=os.getenv('KEY_CREDENTIAL')                        
    )

def item_sets():
    pages = math.ceil(omeka.get_resources("item_sets")["total_results"] / 5)
    item_sets = []
    for i in range(pages):
        item_sets += omeka.get_resources("item_sets", page=i)["results"]
    return item_sets