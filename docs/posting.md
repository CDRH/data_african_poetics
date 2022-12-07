## How to download the files from Airtable and post to API

Note: for the time being, do this step on a local machine and then pull to the data repository on the server.

Make sure you have an API key from Airtable and know the base ID of the tables you want to download.
Create a `.env` file in the base directory of the data repo, it should be automatically be .gitignore'd as secrets should never be committed. Find the base ID by navigating to the project page on airtable, clicking on Help and then "Api Documentation" at the bottom of the sidebar, where it says "The ID of this base is ****". The API key can be found on your account page Add the base ID and API key to `.env`:
```
BASE_ID=app**************
API_KEY=key**************
```
Run `python3 scripts/airtableExport/airtable_to_csv.py`. You may need to first run `pip3 install -r requirements.txt`. The json export from Airtable will be in `scripts/airtableExport/json` and the generated csv files will be in `scripts/airtableExport/csv` and `source/csv` (the latter containing the tables that will be ingested by Datura). The repo is currently set up to ingest news items, commentaries, works, events, and people (poets).

Create and edit `private.yml` and `public.yml` as needed to establish the elasticsearch and API connections.

Run `es_clear_index` to clear the elasticsearch index. Run `post -r [table name]` to post each given table via Datura. For instance, “news items.csv” can be ingested by running `post -r news`.

Running `post` should also work. If not, follow instructions above with the table names that follow for African Poetics:
   - news
   - events
   - people
   - works
   - commentaries
   - contemporary_poets

If any of the above Datura commands fail, try running `bundle` and try again, and then try running `bundle update`.

(Please note: this has only been tested on a Mac. If you want to update files on the dev server it is best to run the scripts on your local machine and push the resulting tables to GitHub, then pull them down from the server)

## How to download image thumbnails

Run `python3 scripts/gale_ingest/python/galeDataExport.py`. This script requires the file `scripts/gale_ingest/output/api_data.csv`. Thumbnail images will be downloaded from Gale and saved into `gale_ingest/source/images/gale`. The script will modify `sources/csv/news items.csv` with the associated image filenames. After running the script you may want to commit these files to git. After running the script, run `post -r news` to post the image filenames to the API.
