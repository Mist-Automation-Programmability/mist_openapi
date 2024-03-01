"""
This script is generating the spec files from the main openapi spec (single file) based on the documentation tag
Can be filtered to one or multiple spec files based on the .filters file
"""
import yaml
import re
import json
import sys

SPEC_FILE_IN="./tmp/mist.openapi_grp3.yml"
FILTER_FILE="./.filters"

with open(FILTER_FILE, 'r') as filter_file:
    filters_string = filter_file.read().split("=")[1].split("#")[0]
    FILTER = filters_string.split(",")

with open(SPEC_FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths")



TAG_NAMES = {
    "MIST": "Mist",
    "WLAN": "Wi-Fi Assurance",
    "LAN": "LAN Assurance",
    "WAN": "WAN Assurance",
    "NAC": "ACCESS Assurance",
    "LOCATION": "Indoor Location",
    "SAMPLES": "Samples",
    "CONSTANTS": "Constants",
    "AUTHENTICATION": "Authentication",
    "MONITOR": "Monitor",
    "CONFIGURE": "Configure"
}

ITEMS = {
    "MIST": {},
    "WLAN": {},
    "LAN": {},
    "WAN": {},
    "NAC": {},
    "LOCATION": {},
    "SAMPLES": {},
}

TAGS = {
    "MIST": [],
    "WLAN": [],
    "LAN": [],
    "WAN": [],
    "NAC": [],
    "LOCATION": [],
    "SAMPLES": [],
}

VERBS = ["get", "post", "put", "delete"]
ORDER = [
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components",
]

OPERATION_IDS = []
for path in PATHS:
    properties = PATHS[path]
    operations = {}
    other_properties = {}
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            operations[verb] = properties[verb]
        else:
            other_properties[verb] = properties[verb]

    for verb, operation in operations.items():
        operation_id = properties[verb]["operationId"]
        tags = []

        for t in properties[verb]["tags"]:
            if t.startswith("tag:"):
                tag = t.replace("tag:","").split(":")[0]
                if not tag in tags:
                    tags.append(tag)

        if len(tags) == 1:
            tag = tags[0]
        else:
            print(f"multiple tags - {operation_id}: {tags}")
        if not path in ITEMS[tag]:
            ITEMS[tag][path]=other_properties
        ITEMS[tag][path][verb] = operation

        for t in properties[verb]["tags"]:
            if not t in TAGS[tag]:
                TAGS[tag].append(t)


REG = r"\"#\/components\/(?P<t>[^\/]*)\/(?P<n>[^\"]*)\""

for tag, operations in ITEMS.items():
    print(f"{tag}".ljust(15), end="")
    if FILTER and tag not in FILTER:
        print("not enabled")
    else:
        print("enabled")
        file = f"./spec/{tag.lower()}/mist.openapi.{tag.lower()}.yml"
        components = {"securitySchemes": data["components"]["securitySchemes"]}
        with open(file, "w")  as oas_out_file:
            for item in ORDER:
                if item == "paths":
                    yaml.dump({item: operations}, oas_out_file)
                    operations_string = json.dumps(operations)
                    refs = re.findall(REG, operations_string)
                    for ref in refs:
                        rtype = ref[0]
                        rname = ref[1]
                        if not rtype in components:
                            components[rtype] = {}
                        if not rname in components[rtype]:
                            components[rtype][rname] = {"$ref": f"../components/{rtype}/{rname}.yml"}
                elif item == "components":
                    yaml.dump({item: components}, oas_out_file)
                elif item == "tags":
                    TAGS_OUT = []
                    for t in data["tags"]:
                        if t.get("name") in TAGS[tag]:
                            TAGS_OUT.append(t)
                    yaml.dump({item: sorted(TAGS_OUT, key=lambda d: d['name'])}, oas_out_file)
                else:
                    yaml.dump({item: data[item]}, oas_out_file)
