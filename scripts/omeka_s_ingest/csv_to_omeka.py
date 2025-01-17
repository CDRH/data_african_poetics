#import necessary modules, including csv and omeka, and the fields
import csv
import omeka
import api_fields

import copy
import json
import markdown
#initialize api and auth info
#TODO can these be refactored as instance variables somehow?

tables = [
    "people",
    "commentaries",
    "events",
    "news items",
    "works"
]

def get_template_number_from_table(table, in_the_news = False):
    #return the number corresponding to the template for the type of item
    #ie news items, events, etc.
    if table == "people" and in_the_news:
        return 11
    if table == "people" and not in_the_news:
        return 2
    match table:
        case "commentaries":
            return 10
        case "events":
            return 4
        case "news items":
            return 5
        case "works":
            return 3

for table in tables:
    #iterate through each table in turn and read each csv row
    with open(f'source/csv/{table}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if table != "people":
            template_number = get_template_number_from_table(table)
        # TODO eventually will need to have a way to split up index of poets and in the news
        # initialize tags array
        tags = []
        for row in reader:
            # if posting the people table, check for items that should not be ingested
            if table == "people":
                # skip Index of Poets
                if not ("In the News" in row["site section"] and
                        row["Completion Status"] == "Publish"  and
                        row["Manual data entry complete"].upper() == "TRUE"):
                    continue
                in_the_news = "In the News" in row["site section"]
                template_number = get_template_number_from_table(table, in_the_news)
            if table == "news items" and "Tags" in row and len(row["Tags"]) > 1:
                # combine with existing list and remove duplicates
                tags = list(set(tags + json.loads(row["Tags"])))
            #check if item is in the API already TODO can this be made more efficient
            if table == "people":
                matching_items = omeka.omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["In the News Unique ID"])
            else:
                matching_items = omeka.omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["Unique ID"])
            if matching_items:
                #if item exists, update item
                if matching_items["total_results"] == 1:
                    print(f"updating item {matching_items["results"][0]["dcterms:identifier"][0]["@value"]}")
                    item_to_update = copy.deepcopy(matching_items["results"][0])
                    updated_item = api_fields.prepare_item(row, table, item_to_update)
                    if updated_item:
                        omeka.omeka_auth.update_resource(updated_item, "items")

                #otherwise, create item from scratch
                elif matching_items["total_results"] == 0:
                    new_item = api_fields.prepare_item(row, table)
                    if new_item:
                        print(f"creating item {new_item['dcterms:identifier'][0]["value"]}")
                        payload = omeka.omeka_auth.prepare_item_payload_using_template(new_item, template_number)
                        # if table == "commentaries":
                        #     html_content = f"<h3>Author(s): {row["creator.name"]}</h3>" + row["Content"] + row["Works Cited"]
                        #     # generate desired path
                        #     file_path = f"scripts/omeka_s_ingest/media_files/{row["Unique ID"]}.html"
                        #     # save html_content in that path
                        #     with open(file_path, "w") as file:
                        #         file.write(html_content)
                        #     try:
                        #         omeka.omeka_auth.add_item(payload, media_files=[file_path], template_id=template_number)
                        #     except:
                        #         print(f"error adding html file for {row['Unique ID']}, omitting")
                        #         #just post item without html if there is an error
                        #         omeka.omeka_auth.add_item(payload, template_id=template_number)
                        #         try:
                        #             omeka.omeka_auth.add_item(payload, template_id=template_number)
                        #         except:
                        #             print(f"error posting {row['Unique ID']}, skipping")
                        omeka.omeka_auth.add_item(payload, template_id=template_number)
                    else:
                        print(f"error creating item {row["Unique ID"]} check spreadsheet")
                #if multiple matches, warn but don't ingest
                else:
                    print(f"multiple matches for {row['Unique ID']}, please check Omeka admin site")
            else:
                break
        for tag in tags:
            new_tag = api_fields.create_tags(tag)
            item_sets = omeka.item_sets()
            #check to make sure tag isn't a duplicate
            if new_tag and not any(item["dcterms:title"][0]["@value"] == new_tag["dcterms:title"][0]["value"] for item in item_sets):
                payload = omeka.omeka_auth.prepare_item_payload(new_tag)
                #class_id=23 should associate item with dcType:Collection resource class
                payload['o:resource_class'] = omeka.omeka_auth.format_resource_id(23, 'resource_classes')
                omeka.omeka_auth.s.post(f'{omeka.omeka.api_url}/item_sets', json=payload, params=omeka.omeka_auth.params)

#need to query the API again at this point so that records can be linked
omeka.reset()
#go through tables again to link records
for table in tables:
    #iterate through each table in turn and read each csv row
    with open(f'source/csv/{table}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # if posting the people table, check for items that should not be ingested
            #check if item is in the API already TODO can this be made more efficient
            #everything should be in the API by now
            if table == "people":
                #again, skip "Index of Poets" and only look for the ones marked to post
                if not ("In the News" in row["site section"] and
                        row["Completion Status"] == "Publish"  and
                        row["Manual data entry complete"].upper() == "TRUE"):
                    continue
                matching_items = omeka.omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["In the News Unique ID"])
            else:
                matching_items = omeka.omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["Unique ID"])
            if matching_items and matching_items["total_results"] == 1:
                #if item exists, update item with linked records
                item_id = matching_items["results"][0]["dcterms:identifier"][0]["@value"]
                print(f"linking records for {item_id}")
                item_to_link = copy.deepcopy(matching_items["results"][0])
                linked_item = api_fields.link_records(row, table, item_to_link)
                try:
                    omeka.omeka_auth.update_resource(linked_item, "items")
                except:
                    print(f"Error updating item {item_id}")
                    pass
                #attach html object to commentaries if it doesn't already exist
                # if table == "commentaries" and not len(linked_item["o:media"]) >= 1:
                #     authors = ", ".join(json.loads(row["creator.name"]))
                #     html_content = f"<h3>Author(s): {row["creator.name"]}</h3>" + row["Content"] + row["Works Cited"]
                #     # generate desired path
                #     file_path = f"scripts/omeka_s_ingest/media_files/{row["Unique ID"]}.html"
                #     # save html_content in that path
                #     media_payload = {
                #         "o:is_public": True,
                #         "data": {
                #             "html": html_content
                #         },
                #         "o:ingester": "html"
                #     }
                #     with open(file_path, "w") as file:
                #         file.write(html_content)
                #     try:
                #         omeka.add_media_to_item(linked_item["o:id"], file_path, payload=media_payload)
                #     except:
                #         print(f"error adding html file for {row['Unique ID']}, omitting")
                
            else:
                #if multiple matches or item not found, display warning
                print(f"skipping {row['Unique ID']}, item not properly ingested")

