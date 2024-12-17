## Airtable Export

Export table data from Airtable using Airtable API

### Files
- airtable.py - Python backend for accessing API and pulling table data
- fields.py - field mapping from airtable fields to csv fields
- airtable_to_csv.py - main program, will pull all data from airtable and export full data into json, as well as using mapping from fields.py to export data to csv.

### Configuration
Will need to setup .env file
Set AirTable baseID and API key in .env file
Sample .env file included

### To run
python3 airtable_to_csv.py

### Run output
Exporting Table: news items
Retrieved 806 records
Exporting Table: events
Retrieved 108 records
Exporting Table: people
Retrieved 1699 records
Exporting Table: works
Retrieved 775 records
Exporting Table: locations
Retrieved 444 records
Exporting Table: publications
Retrieved 6 records
Exporting Table: publishers
Retrieved 258 records
Exporting Table: universities
Retrieved 68 records
Exporting Table: repositories-archives
Retrieved 6 records
Exporting Table: commentaries
Retrieved 7 records
Exporting Table: commentary author
Retrieved 5 records
Exporting Table: work roles [join]
Retrieved 1260 records
Exporting Table: news item roles [join]
Retrieved 3339 records
Exporting Table: educations [join]
Retrieved 128 records

