"""
This script is generating the spec files from the main openapi spec (single file) based on the documentation tag
Can be filtered to one or multiple spec files based on the .filters file
"""
import yaml
import re
import json
import sys
import os
import shutil

SPEC_FILE_IN="../mist.openapi.yml"
SPEC_FOLDER_OUT="../src/spec"
FILTER_FILE="./.filters"

with open(FILTER_FILE, 'r') as filter_file:
    filters_string = filter_file.read().split("=")[1].split("#")[0]
    FILTER = filters_string.split(",")

with open(SPEC_FILE_IN, "r") as f:
    DATA = yaml.load(f, Loader=yaml.loader.SafeLoader)
    INFO = DATA.get("info")
    PATHS = DATA.get("paths")
    COMP = DATA.get("components")

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




ITEMS = {
    "orgs": {},
    "sites": {},
    "msps": {},
    "installer": {},
    "misc": {}
}


TAGS = {
    "orgs": [],
    "sites": [],
    "msps": [],
    "installer": [],
    "misc": [],
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


# def reg_path(path:str, props:dict, out:dict):
#     path_splitted = path.split("/")
#     out_pos = out
#     for path_part in path_splitted:
#         if not path_part in out_pos.get("folders"):
#             out_pos["folders"][path_part] = {"folders": {}, "endpoints": {}, "tags": []}
#         out_pos = out_pos["folders"][path_part]
#     out_pos["endpoints"][path] = props
#     for verb in ["get", "post", "put", "delete"]:
#         if verb in props:
#             for tag in out_pos[verb]["tags"]:
#                 if not tag in out_pos["tags"]:
#                     out_pos["tags"].append(tag)

def clean_out_folder():
    full_path = os.path.join(os.path.curdir, SPEC_FOLDER_OUT)
    shutil.rmtree(full_path)
    os.mkdir(full_path)


def check_folder(folder_path):
    full_path = os.path.join(os.path.curdir, SPEC_FOLDER_OUT, folder_path)
    if not os.path.isdir(full_path):
        os.mkdir(full_path)







#####################################################
clean_out_folder()

for path, properties in PATHS.items():
    path_cat = path.replace("/api/v1/", "").split("/")[0]
    if not path_cat in ITEMS:
        path_cat = "misc"
    
    ITEMS[path_cat][path] = properties
    for verb in VERBS:
        if verb in properties:
            for tag in properties[verb]["tags"]:
                if not tag in TAGS[path_cat]:
                    TAGS[path_cat].append(tag)


API_REG = r"\"#\/components\/(?P<t>[^\/]*)\/(?P<n>[^\"]*)\""
COMP_REG = r"#\/components\/(?P<t>[^\/]*)\/(?P<n>[^\']*)"

api_folder = f"api"
check_folder(api_folder)
for cat, operations in ITEMS.items():
    print(f"{cat}".ljust(15), end="")
    if FILTER and cat not in FILTER:
        print("not enabled")
    else:
        print("enabled")
        part_folder = f"{api_folder}/{cat}"
        check_folder(part_folder)
        file = f"{SPEC_FOLDER_OUT}/{part_folder}/mist.openapi.{cat.lower()}.yml"
        components = {"securitySchemes": DATA["components"]["securitySchemes"]}
        with open(file, "w")  as oas_out_file:
            for item in ORDER:
                if item == "paths":
                    yaml.dump({item: operations}, oas_out_file)
                    operations_string = json.dumps(operations)
                    refs = re.findall(API_REG, operations_string)
                    for ref in refs:
                        rtype = ref[0]
                        rname = ref[1]
                        if not rtype in components:
                            components[rtype] = {}
                        if not rname in components[rtype]:
                            components[rtype][rname] = {"$ref": f"../../components/{rtype}/{rname}.yml"}
                elif item == "components":
                    yaml.dump({item: components}, oas_out_file)
                elif item == "tags":
                    TAGS_OUT = []
                    for t in DATA["tags"]:
                        if t.get("name") in TAGS[cat]:
                            TAGS_OUT.append(t)
                    yaml.dump({item: sorted(TAGS_OUT, key=lambda d: d['name'])}, oas_out_file)
                else:
                    yaml.dump({item: DATA[item]}, oas_out_file)

comp_folder = f"components"
check_folder(comp_folder)
for part in ["parameters", "responses", "schemas"]:
    print(part)
    part_folder = f"{comp_folder}/{part}"
    check_folder(part_folder)

    for file_name, file_data in COMP.get(part).items():
        file_path=f"{SPEC_FOLDER_OUT}/{part_folder}/{file_name}.yml"
        if not file_data.get("title"):
            file_data["title"] = (file_name.replace("_ ", " ")).title()
        file_data_string = yaml.dump(file_data)
        refs = re.findall(COMP_REG, file_data_string)
        file_data_string = re.sub(COMP_REG, "../\\1/\\2.yml", file_data_string)
        with open(file_path, "w") as f_out:
            f_out.write(file_data_string)
