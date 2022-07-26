table_fields = {
  "news items": {
    "airtableID":"airtableID",
	  "title": "title",
    "unique_id": "identifier",
    "Article title": "alternative",
    "Document type": "type",
    # "Content type": "type",
    "Article Date": "date",
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
    "[news items]": "[news items]"
  },
  "people": {
    "airtableID":"airtableID",
    "Unique ID":"identifier",
    "Primary Field": "title",
    "Name last": "n/a",
    "Name given": "n/a",
    "Name alt": "n/a",
    "Major african poet": "type",
    "Date birth": "date_not_before",
    "Place of birth": "Place of Birth",
    "Date death": "date_not_after",
    "Name [Gender]": "extent",
    "Country of nationality": "Country of nationality",
    "Bibliography": "abstract",
    "Short biography": "description",
    "Notes": "Notes",
    "[commentaries]": "[commentaries]",
    "Complete": "Complete",
    "educations [join]": "educations[join]",
    "[events]": "[events]",
    "work roles [join]": "work roles [join]",
    "news item roles [join]": "news item roles [join]",
    "Name [Role] (from news item roles [join])": "Name [Role]",
  },
  "works": {
    "airtableID":"airtableID",
    "Unique ID":"identifier",
    "Primary Field": "title",
    "Title": "alternative",
    "Work type": "type",
    "Year": "date_display",
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
    "news_items": "topics"
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
    "Id": "",
    "Name": "",
    "Content": "",
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
