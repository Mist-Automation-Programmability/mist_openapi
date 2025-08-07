"""
This script is generating the spec files from the main openapi spec (single file) based on the documentation tag
Can be filtered to one or multiple spec files based on the .filters file
"""
import yaml
import re
import json
import sys
import os

SPEC_FILE_IN="../tmp/openapi_grp1.yaml"
SPEC_FOLDER_OUT="../src/spec"
FILTER_FILE="./.filters"
PRE_TAG="op"

with open(FILTER_FILE, 'r') as filter_file:
    filters_string = filter_file.read().split("=")[1].split("#")[0]
    FILTER = filters_string.split(",")

with open(SPEC_FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths")
    TAGS = data.get("tags")
    INFO = data.get("info")

INFO["x-codegen-settings"] = {
    "BrandLabel": "Juniper Networks",
    "EnableAdditionalModelProperties": True,
    "GenerateEnums": False,
    "ProjectName": "MistAPI",
    "ReturnCompleteHttpResponse": True,
    "SortResources": True,
    "enableLogging": True,
    "generateExceptions": False,
    "generateInterfaces": True,
    "generateModels": True,
    "nullify404": True,
    "shortCopyrightNotice": "Copyright \xA9 2024 Juniper Networks, Inc.  All rights reserved",
    "useControllerPrefix": False,
    "useEnumPostfix": True,
    "useMethodPrefix": False,
    "useModelPostfix": False,
    "userAgent": "SDK 2024.2.1",
    "userConfigurableRetries": True
}
INFO["x-server-configuration"] = {
    "default-environment": "Mist Global 01",
    "default-server": "API Host",
    "environments": [
        {
            "name": "Mist Global 01",
            "servers": [
                {"name": "API Host", "url": "https://api.mist.com"}
            ]
        },{
            "name": "Mist Global 02",
            "servers": [
                {"name": "API Host", "url": "https://api.gc1.mist.com"}
            ]
        },{
            "name": "Mist Global 03",
            "servers": [
                {"name": "API Host", "url": "https://api.ac2.mist.com"}
            ]
        },{
            "name": "Mist Global 04",
            "servers": [
                {"name": "API Host", "url": "https://api.gc2.mist.com"}
            ]
        },{
            "name": "Mist EMEA 01",
            "servers": [
                {"name": "API Host", "url": "https://api.eu.mist.com"}
            ]
        },{
            "name": "Mist EMEA 02",
            "servers": [
                {"name": "API Host", "url": "https://api.gc3.mist.com"}
            ]
        },{
            "name": "Mist APAC 01",
            "servers": [
                {"name": "API Host", "url": "https://api.ac5.mist.com"}
            ]
        }
    ]
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

REG = r"\"#\/components\/(?P<t>[^\/]*)\/(?P<n>[^\"]*)\""

for tag_entry in TAGS:
    tag = tag_entry["name"]
    path = f"/{tag.replace('.', '/')}"
    path_tags = []
    if tag.startswith("api.v1"):
        if not os.path.isdir(f"{SPEC_FOLDER_OUT}/{tag}"):
            os.makedirs(f"{SPEC_FOLDER_OUT}/{tag}")
        file = f"{SPEC_FOLDER_OUT}/{tag}/openapi.{tag.lower()}.yaml"
        components = {"securitySchemes": data["components"]["securitySchemes"]}
        for verb in VERBS:
            if PATHS[path].get(verb):
                operation_tags = PATHS[path][verb]["tags"]
                for operation_tag in operation_tags:
                    if not operation_tag in path_tags:
                        path_tags.append(operation_tag)
                        
        with open(file, "w")  as oas_out_file:
            for item in ORDER:
                if item == "paths":
                    yaml.dump({item: {path: PATHS[path]}}, oas_out_file)
                    operations_string = json.dumps(PATHS[path])
                    refs = re.findall(REG, operations_string)
                    for ref in refs:
                        rtype = ref[0]
                        rname = ref[1]
                        if not rtype in components:
                            components[rtype] = {}
                        if not rname in components[rtype]:
                            components[rtype][rname] = {"$ref": f"../components/{rtype}/{rname}.yaml"}
                elif item == "components":
                    yaml.dump({item: components}, oas_out_file)
                elif item == "tags":
                    TAGS_OUT = []
                    for t in data["tags"]:
                        if tag_entry.get("name") in path_tags:
                            TAGS_OUT.append(t)
                    yaml.dump({item: sorted(TAGS_OUT, key=lambda d: d['name'])}, oas_out_file)
                elif item == "info":
                    yaml.dump({item: INFO}, oas_out_file)
                else:
                    yaml.dump({item: data[item]}, oas_out_file)
