""" 
validate every tag has a description
"""

import yaml

FILE_IN = "./mist.openapi.yaml"



with open(FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    TAGS = data.get("tags", [])

COUNT = 0
TOTAL = 0
for tag in TAGS:
    TOTAL += 1
    if not tag.get("description"):
        print(f"description is missing for tag {tag.get('name')}")
        COUNT += 1

print()
print(f"MISSING: {COUNT} / {TOTAL}")
