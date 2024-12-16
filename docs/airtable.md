# Airtable Structure and data documentation

## Tables 

The Airtable contains 5 tables that will be pulled down to populate data. There are many more linked tables, but all the data from linked tables is included through lookup tables in the 5 tables. See below for the data definitions of each field.

These tables are: 

- News Items
- Events
- Works
- People
- Commentaries

## Data format

There are a few kinds of data that will be pulled from airtable, and processing differs depending on the way the data is included

- `Plain text` - these fields can be pulled as is and added to the index
- `Date` - these should always be formatted in ISO format (YYYY-MM-DD) in Airtable. If dates were entered differently, there is a function in Airtable to normalize into the standard format, so this should not have to be done with pulldown scripts
- `Array` - These are array fields coming from airtable, which will be a JSON array of items
- `Manual Array` - These are manually created arrays, to be split on `;;;`. These are created because of limitations on creating arrays in Airtable
- `Markdown` - much of the data is formatted in a Markdown Link like format `[Name of thing](id of thing)` - sometimes these will be parsed to add values to individual fields like name.role and name.id, but other times they will be indexed as is an parsed on the front end
- `Markdown + Role` - some fields need to link to an item and also indicate a role, and will look like `[Thing Name](thing id)|Role Name`. These entries will need to be parsed to add to individual fields


## How to update airtable field names:

Modify `scripts/airtableExport/fields.py`. Each key corresponds to an airtable column name (which will be repeated in the csv), and the values to the api field where it will be stored.
If the field in question is an array, add the column name to the following array in `airtable_to_csv.py` so that it can be properly parsed as JSON:
```
    records = tables[table]
    for record in records.values():
        for key, value in record['fields'].items():
            if key in ["source", "Tags”,.. ]#INSERT MORE COLUMN NAMES HERE
```
 You may need to run the `airtable_to_csv.py` script and look at `scripts/airtableExport/tables.json` to determine the format of the downloaded field.
When the output is to your satisfaction, run the scripts again to update your tables.
