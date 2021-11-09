## Gale Api Data Export

Read in gale document ids from the second column at gale_ingest/input/gale_ids.csv file. 
Retrieve the document data through the gale api for each id.
Write the document data to csv file at gale_ingest/output/api_data.csv.

To run: 
python3 galeDataExport.py

Wrote code for most of the data elements in the json documents from gale

Ommitted data is all from the page data, such as height/width on images, image id, and clip coordinates.

### Current data
#### Doc data
	id
	title
	description
	authors
	publication title
	publication date
	publication issue Number
	publication issn
	content type
	start page
	word count
	subjects
	rights
	citation
	isShownAt (url)

#### Page Response Data
	docId
	dviType
	image urls
	image ocr text
	full text ocr
	


Currently there are quite a few elements commented out, but can be added back in if needed.

Output is generated in the order of the keys as the data is added for each record, so if a different ordering is needed these might need to be shuffled around.



