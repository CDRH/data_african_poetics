import requests
import json
import csv
import re
from pathlib import Path

# Function to call gale api and generate key using institutional user id
def generateKey(user):
	server = "https://api.gale.com/"
	service = "api/tools/generate_key"
	URL = server + service

	PARAMS = {}
	PARAMS["user"] = user

	r = requests.get(url=URL, params=PARAMS)
	return r.json()

# Function to retrieve gale record json using document id and api key
def retrieveDocument(doc_id, apiKey):
	server = "https://api.gale.com/"
	service = "api/v1/item/"
	URL = server + service + doc_id

	PARAMS = {}
	PARAMS["api_key"] = apiKey

	r = requests.get(url = URL, params = PARAMS)
	return r.json()



# Extract gale document ids from csv file
gale_ids = []
script_loc = Path(__file__).parent
input_relative = "../input/gale_ids.csv"
input_filename = (script_loc / input_relative).resolve()
with open(input_filename,'r') as csvfile:
	csvreader = csv.reader(csvfile)
	next(csvreader) # skip header row
	for row in csvreader:
		gale_ids.append(row[1].strip())
		

# Get api key from gale using institutional id
user = 'linc74325' #Institutional ID
apiKey = generateKey(user)['apiKey']

# Retreive the document json from gale and 
# store data into records by key/value
rows=[]
for id in gale_ids:
	#check if this column is composed of urls, if so extract the id
	url_match = re.match("https:\/\/.*?\/apps\/doc\/(.*?)\/", id)
	if url_match:
		id = "GALE|" + url_match.group(1)
	data = retrieveDocument(id,apiKey)
	print('Retreived doc: '+id)

	record = {}

	# Process doc data
	if 'doc' in data:
	#	record['id'] = data['doc']['id']
		record['title'] = data['doc']['title']
	#	record['description'] = data['doc']['description']
		
		if 'authors' in data['doc']:
			record['authors'] = data['doc']['authors']
		else:
			record['authors'] =''

		record['pub_title'] = data['doc']['publication']['title']
		record['pub_date'] = data['doc']['publication']['date']
		
		if 'issueNumber' in data['doc']['publication']: 
			record['pub_issuenum'] = data['doc']['publication']['issueNumber']
		else:
			record['pub_issuenum']=''

	#	record['pub_issn'] = data['doc']['publication']['issn']
	#	record['content_type'] = data['doc']['contentType']
		
		if 'startPage' in data['doc']: 
			record['start_page'] = data['doc']['startPage']
		else:
			record['start_page'] =''
		
	#	record['word_count'] = data['doc']['wordCount']
		
		if 'subjects' in data['doc']:
			record['subjects'] = data['doc']['subjects']
		else:
			record['subjects']=''

	#	record['rights'] = data['doc']['rights']
		record['citation'] = data['doc']['citation']
		record['url'] = data['doc']['isShownAt']



		# Process pageResponse data

		record['doc_id'] = data['pageResponse']['docId']
		record['dvi_type'] = data['pageResponse']['dviType']

		pages = data['pageResponse']['pages']
		image_url = []
		image_ocr = []
		for page in pages:
			image_url.append(page['image']['url'])
			if "ocrText" in page:
				image_ocr.append(page['ocrText'])
			else:
				image_ocr.append("")

		record['image_url'] = image_url
	#	record['image_ocr'] = image_ocr
	#	record['full_ocr_text'] = data['pageResponse']['fullOcrText']

	rows.append(record)


# Export data to csv file
keys = rows[0].keys()
output_relative = "../output/gale_ids.csv"
output_filename = (script_loc / output_relative).resolve()
with open(output_filename, 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(rows)


