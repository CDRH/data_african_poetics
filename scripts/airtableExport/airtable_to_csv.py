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
	header = list(table_fields[table].keys())
	csvfile = open('scripts/airtableExport/csv/'+table+'.csv', 'w')
	writer = csv.DictWriter(csvfile,fieldnames=header,extrasaction='ignore',quoting=csv.QUOTE_ALL)
	
	
	writer.writeheader()

	records = tables[table]
	for record in records.values():
		for key, value in record['fields'].items():
			if key in ["source", "Tags"]:
				record['fields'][key] = json.dumps(value)
		writer.writerow(record['fields'])

	csvfile.close()
