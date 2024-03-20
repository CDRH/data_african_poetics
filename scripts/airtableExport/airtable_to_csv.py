import json
import time
import csv

import airtable
import fields

tables = {
	'news items':{},
	'events':{},
	'people':{},
	'works':{},
	'locations':{},
	'publications':{},
	'publishers':{},
	'universities':{},
	'repositories-archives':{},
	'commentaries':{},
	'commentary author':{},
	'work roles [join]':{},
	'news item roles [join]':{},
	'educations [join]':{}
}

table_fields = fields.table_fields

def getTables():
	for table in tables:
		print('Exporting Table: '+table)
		# call airtable.py to get records in the form of a hash
		records = airtable.getTable(table)
		print('Retrieved '+ str(len(records)) +' records')
		tables[table] = records
		#wait to not overload api
		time.sleep(1)

getTables()

with open('scripts/airtableExport/json/tables.json','w') as f:
	json.dump(tables,f,indent=2)

# with open('scripts/airtableExport/json/tables.json','r') as f:
# 	table_json = json.load(f)


#Export tables to csv
for table in tables:
	# read in the keys defined in fields.py
	header = list(table_fields[table].keys())
	if table in ["commentaries", "events", "news items", "people", "works"]:
		csvfile = open('source/csv/'+table+'.csv', 'w')
	else:
		csvfile = open('scripts/airtableExport/csv/'+table+'.csv', 'w')
	writer = csv.DictWriter(csvfile,fieldnames=header,extrasaction='ignore',quoting=csv.QUOTE_ALL)
	
	
	writer.writeheader()
	records = tables[table]
	for record in records.values():
		# make sure that each cell in the csv, if stored as an array, can be parsed as json
		for key, value in record['fields'].items():
			if key in ["source", "Tags", "spatial.country", "spatial.city", "spatial.region", "rights_holder", "publisher", "contributor.name", "creator.name", "publisher", "person-notpoet", "person-poet", "name-major-poet", "person-author", "news_items", "commentaries_relation", "nationality-region", "nationality-country", "education", "events", "birth_spatial.country", "birth_spatial.city", "year_degree_institution", "events-subjects", "works", "news-items_medium", "news item roles", "site section", "work roles", "person", "subjects"]:
				record['fields'][key] = json.dumps(value)
		writer.writerow(record['fields'])

	csvfile.close()
