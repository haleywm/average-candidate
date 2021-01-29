import download
import markovify
import requests
import facemorpher
from urllib.parse import urlparse
from os.path import basename
from os import makedirs
import random

def scrape(candidate_urls, link_sel, pic_sel, name_sel, desc_sel, output_folder):
    # Emptying the output folder if it exists
    makedirs(output_folder, exist_ok=True)
    urls = list()
    for candidate in candidate_urls:
        urls += download.get_links(candidate, link_sel)

    data = {"images": list(), "names": list(), "text": None}
    
    for url in urls:
        page_data = download.get_page_values(url, [(pic_sel, "src"), (name_sel, None), (desc_sel, None)])
        if page_data[0]:
            data["images"].append(page_data[0])
        if page_data[1]:
            data["names"].append(page_data[1])
        if isinstance(page_data[2], str) and len(page_data[2].strip()) > 0:
            if data["text"] is None:
                data["text"] = markovify.Text(page_data[2].strip())
            else:
                data["text"] = markovify.combine([data["text"], markovify.Text(page_data[2].strip())])
    
    # Now I have a list of images url's and names, as well as an already built markov model.
    data["text"] = data["text"].compile()
    print("Downloading images..")
    for image_url in data["images"]:
        print("Getting " + image_url + "...")
        image = requests.get(image_url)
        with open(output_folder + "/" + basename(urlparse(image_url).path), "wb") as file:
            file.write(image.content)

    print("Merging images...")
    image_paths = facemorpher.list_imgpaths(output_folder)
    facemorpher.averager(image_paths, out_filename=output_folder + "/average.jpg", background="average")

    print("Generating text...")
    text = generate_text(data["text"])
        
    return text

def generate_text(generator):
    # Generates text and returns it
    SENTANCES_PER_PARA = (2, 5)
    PARAGRAPHS = (4, 8)

    paras = random.randrange(PARAGRAPHS[0], PARAGRAPHS[1] + 1)
    output = ""

    for _ in range(paras):
        sentances = random.randrange(SENTANCES_PER_PARA[0], SENTANCES_PER_PARA[1] + 1)
        for _ in range(sentances):
            output += generator.make_sentence() + " "
        output = output[:-1] + "\n\n"
    
    return output

def generate_output(template_loc, text, out_loc):
    if template_loc:
        try:
            with open(template_loc) as file:
                to_replace = file.read()
            to_replace = to_replace.replace("$PICTURE_SOURCE$", "faces/average.jpg", 1)
            to_replace = to_replace.replace("$DESCRIPTION_TEXT$", text, 1)
            with open(out_loc + "index.html", "w") as file:
                file.write(to_replace)
        except FileNotFoundError:
            template_loc = None
    if template_loc is None:
        # No template to work with, will just write to file
        with open(out_loc + "text.txt", "w") as file:
            file.write(text)