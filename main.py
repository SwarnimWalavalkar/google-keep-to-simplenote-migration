import simplenote
import json
import os

# Load and init dotenv
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Init Simplenote API with username and pass from a .env file
sn = simplenote.Simplenote(
    os.environ.get("EMAIL"), os.environ.get("PASS"))

# Make sure your google takeout json files are in a "data" folder
for filename in os.listdir("./data"):
    print(filename, type(filename))
    # open every file in the folder
    with open(os.path.join("./data/", filename)) as file:
        # Load the json data
        try:
            data = json.load(file, encoding="utf-8")
        except:
            print("couldn't open file")
            continue

        # Build the "Note" object to uplaod to simplenote
        content = ""

        # Skip empty notes
        if (len(data["title"]) <= 0 and len(data["textContent"]) <= 0):
            print("file skipped")
            continue

        # Concatenate data.title and data.textContent to a single content parameter (based on the required simplenote note schema)
        if (len(data["title"]) > 0):
            content += data["title"] + "\n"

        content += data["textContent"]

        # Get tags from json
        tags = []
        if ("labels" in data):
            for label in data["labels"]:
                # Replace spaces with "-" in label names (simplenote doesnt support spaces in label names)
                tags.append(label["name"].replace(" ", "-"))

        # Create a new note object with all the extracted data to uplaod to simplenote
        note = {
            "content": content,
            "tags": tags
        }

        # Upload to simplenote
        sn.add_note(note)
