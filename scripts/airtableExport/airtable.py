import requests
import json
from pathlib import Path
import time
import os
from dotenv import load_dotenv
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

server = os.getenv('AIRTABLE_SERVER')
base_id = os.getenv('BASE_ID')
api_key = os.getenv('API_KEY')

if base_id == None:
	print('Make sure base_id is set')
	exit()
if api_key == None:
	print('Make sure api_key is set')
	exit()

def getTable(table):
	records = {}

	url = server+base_id+'/'+table
	HEADERS = {'Authorization':'Bearer '+api_key}
	PARAMS = {'view':'Grid view'}
	
	res = requests.get(url, params = PARAMS, headers = HEADERS)
	data = res.json()
	for record in data['records']:
		record['fields']['airtableID'] = record['id']
		records[record['id']] = record

	count = 1
	while 'offset' in data:
		if count % 5 == 0:
			time.sleep(1) # wait to not overload api
			
		PARAMS['offset']=data['offset']
		res = requests.get(url, params = PARAMS, headers = HEADERS)
		data = res.json()
		for record in data['records']:
			records[record['id']] = record
		
		count = count + 1
	
	return records

