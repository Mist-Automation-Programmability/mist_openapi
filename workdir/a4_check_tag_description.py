""" 
validate every tag has a description
"""

import yaml

FILE_IN = "./mist.openapi.yml"



with open(FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    TAGS = data.get("tags", [])

for tag in TAGS:
    if not tag.get("description"):
        print(f"description is missing for tag {tag.get('name')}")
