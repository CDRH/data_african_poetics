import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
from omeka_s_tools.api import OmekaAPIClient
omeka = OmekaAPIClient('http://libr-cdrh2102vs3.unl.edu/omeka-s/api')
omeka_auth = OmekaAPIClient(
    api_url = 'http://libr-cdrh2102vs3.unl.edu/omeka-s/api',
    key_identity=os.getenv('KEY_IDENTITY'),                        
    key_credential=os.getenv('KEY_CREDENTIAL')                        
)