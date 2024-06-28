import csv
import omeka
import markdown
import json

with open(f'source/csv/people.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # if posting the people table, check for items that should not be ingested
        #check if item is in the API already TODO can this be made more efficient
        #everything should be in the API by now
        matching_items = omeka.omeka.filter_items_by_property(filter_property = "dcterms:identifier", filter_value = row["Unique ID"])
        if matching_items and "Index of Poets" in row["site section"]:
            if matching_items["total_results"] == 1:
                matching_item = matching_items["results"][0]
            elif matching_items["total_results"] > 1:
                # make sure to find the one that is Index of Poets if there are multiple
                # I think it should be unique now so this shouldn't happen
                print("multiple items found for " + row["Unique ID"] + ", check admin site")
            else:
                print("no matching items for " + row["Unique ID"])
                continue
            if len(row["Biography"]) > 10 and not len(matching_item["o:media"]) >= 1:
                print("adding media for " + row["Unique ID"])
                biography = markdown.markdown(row["Biography"])
                html_content = f"<h3>Biography</h3>" + biography 
                if len(row["Bio Sources (MLA)"]) > 10:
                    sources = markdown.markdown(row["Bio Sources (MLA)"])
                    html_content += f"<h3>Sources Cited</h3>" + sources
                # generate desired path
                file_path = f"scripts/omeka_s_ingest/media_files/{row["Unique ID"]}.html"
                # save html_content in that path
                media_payload = {
                    "o:is_public": True,
                    "data": {
                        "html": html_content
                    },
                    "o:ingester": "html"
                }
                with open(file_path, "w") as file:
                    file.write(html_content)
                try:
                    omeka.add_media_to_item(matching_item["o:id"], file_path, payload=media_payload)
                except:
                    print(f"error adding html file for {row['Unique ID']}, omitting")
        else:
            print("no match for " + row["Unique ID"])
