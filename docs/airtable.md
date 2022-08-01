# Airtable Structure and data documentation

## Tables 

The Airtable contains 5 tables that will be pulled down to populate data. There are many more linked tables, but all the data from linked tables is included through lookup tables in the 5 tables. 

These tables are: 

- News Items
- Events
- Works
- People
- Commentaries

TODO: bring in the tables describing these tables once the data transfer is done

- https://github.com/CDRH/african_poetics/issues/225
- https://github.com/CDRH/african_poetics/issues/224
- https://github.com/CDRH/african_poetics/issues/223
- https://github.com/CDRH/african_poetics/issues/226
- https://github.com/CDRH/african_poetics/issues/246

## Data format

There are a few kinds of data that will be pulled from airtable, and processing differs depending on the way the data is included

- `Plain text` - these fields can be pulled as is and added to the index
- `Date` - these should always be formatted in ISO format (YYYY-MM-DD) in Airtable. If dates were entered differently, there is a function in Airtable to normalize into the standard format, so this should not have to be done with pulldown scripts
- `Array` - These are array fields coming from airtable, which will be a JSON array of items
- `Manual Array` - These are manually created arrays, to be split on `;;;`. These are created because of limitations on creating arrays in Airtable
- `Markdown` - much of the data is formatted in a Markdown Link like format `[Name of thing](id of thing)` - sometimes these will be parsed to add values to individual fields like name.role and name.id, but other times they will be indexed as is an parsed on the front end
- `Markdown + Role` - some fields need to link to an item and also indicate a role, and will look like `[Thing Name](thing id)|Role Name`. These entries will need to be parsed to add to individual fields
