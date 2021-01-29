import os
from shutil import rmtree
import scraper
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

LOCATION = os.path.dirname(__file__) + "/"

def main():
    with open(LOCATION + "sources.yml") as file:
        config = load(file, Loader=Loader)
    print("Average Candidate Generator")
    print("Please choose an option to generate: (Leave empty for all)")

    for option in config.keys():
        print("  - " + option)
    
    choice = input()
    if len(choice) == 0:
        # Doing all
        print("Doing all options...")
        for key, value in config.items():
            print("Doing " + key + "...")
            process_option(key, value)
    else:
        if choice in config:
            # Doing one
            print("Doing " + choice + "...")
            process_option(choice, config[choice])
        else:
            print("Invalid option")

def process_option(option_name, option):
    # Removing the output folder if it exists to clean up
    rmtree(LOCATION + "output/" + option_name, ignore_errors=True)

    text = scraper.scrape(option["list-urls"],
        option["link-selector"],
        option["image-selector"],
        option["name-selector"],
        option["description-selector"],
        LOCATION + "output/" + option_name + "/faces",
        LOCATION + "output/" + option_name + "/avg" + option_name + ".jpg"
    )
    scraper.generate_output(LOCATION + "templates/" + option["template"], text, LOCATION + "output/" + option_name + "/")


if __name__ == "__main__":
    main()