import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
from omeka_s_tools.api import OmekaAPIClient
import math
omeka = OmekaAPIClient('https://libr-cdrh2102vs3.unl.edu/apdp/api')
omeka_auth = OmekaAPIClient(
    api_url = 'https://libr-cdrh2102vs3.unl.edu/apdp/api',
    key_identity=os.getenv('KEY_IDENTITY'),                        
    key_credential=os.getenv('KEY_CREDENTIAL')                        
)

def reset():
    omeka = OmekaAPIClient('https://libr-cdrh2102vs3.unl.edu/apdp/api')
    omeka_auth = OmekaAPIClient(
        api_url = 'https://libr-cdrh2102vs3.unl.edu/apdp/api',
        key_identity=os.getenv('KEY_IDENTITY'),                        
        key_credential=os.getenv('KEY_CREDENTIAL')                        
    )

def item_sets():
    pages = math.ceil(omeka.get_resources("item_sets")["total_results"] / 5)
    item_sets = []
    for i in range(pages):
        item_sets += omeka.get_resources("item_sets", page=i)["results"]
    return item_sets