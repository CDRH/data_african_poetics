def prepare_item(row):
    item_dict = {
        "dcterms:title": [
            {
                "value": row["Name Built"]
            }
        ]
    }
    return item_dict
