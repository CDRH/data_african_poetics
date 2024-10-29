table_fields = {
  "news items": {
    "airtableID":"airtableID",
	  "title": "title",
    "Unique ID": "identifier",
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
    "Completion Status": "Complete",
    "person": "person",
#    "autonumber": "",
#    "autonumber copy": "",
#    "Summary": ""
    "contributor.name": "contributor.name",
    "creator.name": "creator.name",
    "topics-decade": "topics",
    "commentaries_relation": "relation",
    "Related Event Omeka ID": "dcterms:relation", 
    "Contributor Omeka ID": "dcterms:references", 
    "Publication Internal ID": "dcterms:publisher",
    "site section": "bibo:section"
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
    "topics-decade": "topics",
    "places": "places",
    "spatial.region": "spatial.region",
    "spatial.country": "spatial.country",
    "spatial.city": "spatial.city",
    "commentaries_relation": "relation",
    "news_items": "medium",
    "Location (Country)": "dcterms:spatial",
    "Location (City)": "foaf:based_near",
    "Event Type": "dcterms:type",
    "Related News Item Omeka ID": "dcterms:isReferencedBy",
    "Related Poet Omeka ID": "dcterms:subjects",
    "events-subjects": "dcterms:references",
    "works": "dcterms:relation",
    "Latitude (from [location])": "latitude",
    "Longitude (from [location])": "longitude",
    "spatial.place": "spatial.place",
    "site section": "bibo:section"
  },
  "people": {
    "airtableID":"airtableID",
    "Unique ID":"identifier",
    "Name Built": "title",
    "Major african poet": "type",
    "Featured": "type",
    "nationality-country": "places",
    "Biography": "description",
    "name-letter": "alternative",
    "education": "keywords",
    "year_degree_institution": "keywords",
    "events": "subjects",
    "work roles": "works",
    "news item roles": "medium",
    "birth-decade": "topics",
    "nationality-region": "spatial.region",
    "Date birth": "date_not_before",
    "Date death": "date_not_after",
    "birth_spatial.country": "spatial.country",
    "birth_spatial.city": "spatial.city",
    "related-people": "people",
    "commentaries_relation": "relation",
    "site section": "subcategory",
    "Name last": "person.name",
    "Name given": "person.name",
    "Bio Sources (MLA)": "source",
    "death place": "spatial_name_death_k",
    "Languages spoken": "language",
    "Gender": "person.gender",
    "In the News Unique ID": "dcterms:references",
    "University Omeka ID": "foaf:maker",
    "Related News Item Omeka ID": "foaf:isPrimaryTopicOf",
    "Related Event Item ID": "dcterms:isReferencedBy",
    "Related Works Omeka Item ID": "foaf:made",
    "Completion Status": "complete",
    "Manual data entry complete": "complete",
    "Place of Birth Omeka ID": "geo:location",
    "Latitude (from Place of birth)": "latitude",
    "Longitude (from Place of birth)": "longitude",
    "site section": "bibo:section",
    "Number of linked News Items": "curation:number",
    "Poems": "poems_k",
    "Poetry Collections": "poetry_collections_k",
    "speeches lectures": "speeches_k",
    "ethnicity.text": "ethnicity_k",
    "country_residence.text": "country_residence_k"
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
    "topics-decade": "topics", 
    "commentaries_relation": "relation",
    "[commentaries]": "dcterms:isReferencedBy",
    "References": "dcterms:references",
    "site section": "bibo:section"
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
    "person-poet": "person.name",
    "creator.name": "creator.name",
    "events-subjects": "subjects",
    "works": "works",
    "news-items_medium": "medium",
    "Events Omeka ID": "dcterms:references",
    "News Item Omeka ID": "bibo:cites",
    "Referenced Poet Omeka ID": "dcterms:subject",
    "Works Omeka ID": "dcterms:relation",
    "Works Cited": "dcterms:bilbiographicalCitation" 
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
