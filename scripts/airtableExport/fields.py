table_fields = {
  "news items": {
    "airtableID":"airtableID",
	  "title": "title",
    "unique_id": "identifier",
    "Article title": "alternative",
    "Document type": "type",
    # "Content type": "type",
    "Article Date (formatted)": "date",
    "[publication]": "[publication]",
    "publisher": "publisher",
    "Source page no": "page_k",
    "Source link": "rights_uri",
    "Gale ID": "identifer_origin_k",
    "Source access date": "date_not_after",
    "rights_holder": "rights_holder",
    "[archive]": "[archive]",
    "Excerpt": "description",
    "works": "works",
    "[events]": "events",
    "subjects": "subjects",
    #"Commentaries": "",
    "Tags": "keywords",
    "Notes": "[notes]",
    "Permissions": "rights",
    "[news item roles]": "[news item roles]",
    "Complete": "Complete",
    "person": "person",
#    "autonumber": "",
#    "autonumber copy": "",
#    "Summary": ""
    "contributor.name": "contributor.name",
    "creator.name": "creator.name",
    "topics-decade": "topics",
    "commentaries-link": "relation"
  },
  "events": {
    "airtableID":"airtableID",
    "Unique ID": "identifier",
    "Primary Field": "n/a",
    "Name": "title",
    "Date not before": "date_not_before",
    "Date": "date",
    "Summary": "description",
    "[location]": "[location]",
    "Event type": "type",
    "Complete": "Complete",
    "[commentaries]": "[commentaries]",
    "[people]": "[people]",
    "[news items]": "[news items]",
    "person-notpoet": "person.name",
    "person-poet": "person",
    "topics-decades": "topics",
    "places": "places",
    "spatial.region": "spatial.region",
    "spatial.country": "spatial.country",
    "spatial.city": "spatial.city",
    "commentaries_relation": "relation",
    "news_items": "medium"
  },
  "people": {
    "airtableID":"airtableID",
    "Unique ID":"identifier",
    "Name Built": "title",
    "Major african poet": "type",
    "nationality-country": "places",
    "short biography": "description",
    "name-letter": "alternative",
    "education": "keywords",
    "events": "subjects",
    "work roles": "works",
    "news item roles": "medium",
    "birth-decade": "topics",
    "nationality-region": "spatial.region"
  },
  "works": {
    "airtableID":"airtableID",
    "Unique ID":"identifier",
    "Primary Field": "title",
    "Title": "alternative",
    "Work type": "type",
    "Year": "date.year",
    "publisher": "publisher",
    "spatial.country": "spatial.country",
    "spatial.city": "spatial.city",
    "Page no": "page_k",
    "Issue":"issue_k",
    "Volume":"volume_k",
    "Source link": "rights_uri",
    "[commentaries]": "commentaries_k",
    "person": "person",
    "Complete": "Complete",
    "news_items": "medium",
    "name-major-poet": "contributor.name",
    "person-author": "creator.name",
    "topics-decade": "topics"
  },
  "locations": {
    "airtableID":"",
    "Primary Field": "",
    "Place": "",
    "Local place": "",
    "City": "",
    "County/township": "",
    "State/province/territory": "",
    "Country": "",
    "Latitude": "",
    "Longitude": "",
    "Name [Region]": "",
    "[Universities]": "",
    "[events]": "",
    "[people] Country of Nationality": "",
    "[people] Place of Birth": "",
    ":[works]": "",
    "[publications]": "",
    "[publishers]": "",
#    "[repositories-archives]":""
  },
  "publications": {
    "airtableID":"",
    "Id": "",
    "Name": "",
    "[location]": "",
    "[repository]": "",
    "[news items]": ""
  },
  "publishers": {
    "airtableID":"",
    "Primary field": "",
    "Name": "",
    "[location]": "",
    "[works]": "",
    "Count (works)": ""
  },
  "universities": {
    "airtableID":"",
    "Id": "",
    "Name": "",
    "[locations]": "",
    "educations [join]": ""
  },
  "repositories-archives": {
    "airtableID":"",
    "Id": "",
    "Name": "",
#    "Id [Location]":"",
    "[news items]": "",
    "Count (news items)": "",
    "publications": ""
  },
  "commentaries": {
    "airtableID":"",
    "Unique ID": "identifier",
    "Name": "title",
    "Content": "text",
    "Featured": "",
#    "Id [Metacommentary objects]":"",
#    "Id [Subjects]":"",
#    "Name [Subjects]":"",
#    "Id [Metacommentary subjects]":"",
#    "Id [Meta objects]":"",
#    "Name [Meta objects]":"",
    "[commentary author]": "",
    "[news items]": "",
    "[people]": "",
    "[works]": "",
    "[events]": ""
  },
  "commentary author": {
    "airtableID":"",
    "primary field": "",
    "Name last": "",
    "Name given": "",
    "Name title": "",
    "Short biography": "",
    "[commentaries]": ""
#    "Id copy": ""   
  },
  "work roles [join]": {
    "airtableID":"",
    "Primary Field": "",
    "Author": "",
    "[person]": "",
    "[works]": "",
    "Name [Role]": ""
#    "Primary Field copy": ""
  },
  "news item roles [join]": {
    "airtableID":"",
    "Id": "",
    "Author": "",
    "[person]": "",
    "[news item]": "",
    "Name [Role]": ""
  },
  "educations [join]": {
    "airtableID":"",
    "Id": "",
    "[person]": "",
    "[universities]": "",
    "Year ended": "",
    "Graduated": "",
    "Degree": "",
    "Complete": ""
#    "Id copy": ""
  }
}
