## How to download the files from Airtable and post to API

Note: it is necessary to do this step on a local machine, commit to git and push to GitHub, and then pull to the data repository on the server.

Make sure you have an acceess token key from Airtable and know the base ID of the tables you want to download. Note that Airtable has transitioned to a new account system and that you now need to create a [personal access token](https://airtable.com/developers/web/guides/personal-access-tokens). When creating the token, give yourself read access for all options (no need for write access) and select the APDP table. The access token can be found on your account page.
 Find the base ID by navigating to the project page on airtable, clicking on Help and then "Api Documentation" at the bottom of the sidebar, where it says "The ID of this base is ****".   Create a `.env` file in the base directory of the data repo, it should be automatically be .gitignore'd as secrets should never be committed.  The token is still be labeled API_KEY for the sake of the authentication system. Add it along with the BASE_ID to `.env`:
```
BASE_ID=app**************
API_KEY=*****************
```
Run `python3 scripts/airtableExport/airtable_to_csv.py`. You may need to first run `pip3 install -r requirements.txt`. If you have a newer version of macOS, you may also need to set up a [virtual environment]([https://docs.python.org/3/library/venv.html#creating-virtual-environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)) with `python -m venv .venv` and activate it with `source .venv/bin/activate`, before running the pip commands. The json export from Airtable will be in `scripts/airtableExport/json` and the generated csv files will be in `scripts/airtableExport/csv` and `source/csv` (the latter containing the tables that will be ingested by Datura). The repo is currently set up to ingest news items, commentaries, works, events, and people (poets). Commit these files in git and push to GitHub. if you want to save and share these changes.

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

Run `python3 scripts/gale_ingest/python/galeImageDownload.py`. This script requires the file `scripts/gale_ingest/output/gale_ids.csv`. Thumbnail images will be downloaded from Gale and saved into `gale_ingest/source/images/gale`. The script will modify `sources/csv/news items.csv` with the associated image filenames. After running the script you may want to commit these files to git. After running the script, run `post -r news` to post the image filenames to the API.
