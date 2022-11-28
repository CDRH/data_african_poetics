import pandas as pd
from pathlib import Path
import ast
import requests
from PIL import Image
from io import BytesIO
import os

# open the spreadsheet file and get the image column
cwd = Path.cwd()
gale_relative = "scripts/gale_ingest/output/api_data.csv"
gale_path = (cwd / gale_relative).resolve()
gale_frame = pd.read_csv(gale_path)
images = gale_frame[["image_url"]].to_numpy()
# open the news items.csv file
news_relative = "source/csv/news items.csv"
news_path = (cwd / news_relative).resolve()
news_frame = pd.read_csv(news_path)
image_size = (120, 120)
news_frame["has_part_image"] = ""
# iterate through images
for image_cell in images:
    image_list = ast.literal_eval(image_cell[0])
    image_names = ""
    gale_id = gale_frame.loc[gale_frame["image_url"] == image_cell[0], "doc_id"].tolist()[0]
    for image_url in image_list:
        # check if image already exists
        image_name = image_url.split("/")[-1] + ".jpg"
        image_relative = "source/images/gale/" + image_name
        filename = (cwd / image_relative).resolve()
        if not os.path.isfile(filename):
            # download image
            # transform image (resize, change into JPEG)
            # save image to source/images/gale
            request = requests.get(image_url)
            image = Image.open(BytesIO(request.content))
            image_names = image_name if (image_names == "") else (image_names + "; " + image_name)
            image_relative = "source/images/gale/" + image_name
            filename = (cwd / image_relative).resolve()
            try:
                with image as im:
                    im.thumbnail(image_size)
                    print("saving " + image_name)
                    im.save(filename, "JPEG")
            except OSError:
                print("cannot create thumbnail for", image_name)
    # get associated item by Gale id
    # add list of images to column 'has_part_image'
    news_frame.loc[news_frame["Gale ID"] == gale_id, "has_part_image"] = image_names
# save changes to csv
news_frame.to_csv(news_path, index="false")
