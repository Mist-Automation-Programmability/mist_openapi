"""
This script is generating the toc files from the main openapi spec (single file) based on the documentation tag
Can be filtered to one or multiple spec files based on the .filters file
"""

import re
import os
import sys
import yaml
import shutil

SPEC_FILE_IN = "./mist.openapi.yml"
TOC_FOLDER = "../src/content/api"
FILTER_FILE = "./.filters"
ROOT_ITEMS = [
    "self",
    "admins",
    "sites",
    "orgs",
    "msps",
    "installer",
    "utilities",
    "constants",
    "samples",
]


with open(FILTER_FILE, "r") as filter_file:
    filters_string = filter_file.read().split("=")[1].split("#")[0]
    FILTER = filters_string.split(",")

with open(SPEC_FILE_IN, "r") as f:
    DATA = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = DATA.get("paths")
    TAGS = DATA.get("tags")

OPERATION_IDS = []
TOC_API_ITEMS = {"root": []}

for item in ROOT_ITEMS:
    TOC_API_ITEMS["root"].append({"dir": item, "group": item.title()})


############################################################
## POST PROCESSING
def post_processing(file_path):
    print(file_path)
    re_one = r"([ ]*)- generate:\n([ ]*)  (endpoint-group: .*)\n([ ]*)  (from: .*)"
    re_two = r"([ ]*)- generate:\n([ ]*)  (endpoint-group: .*)\n([ ]*)  (endpoint-name: .*)\n([ ]*)  (from: .*)"
    with open(file_path, "r") as f_in:
        data = f_in.read()

    data = re.sub(re_one, "\\1- generate:\n\\2\\3\n\\4\\5", data)
    data = re.sub(re_two, "\\1- generate:\n\\2\\3\n\\4\\5\n\\6\\7", data)
    with open(file_path, "w") as f_out:
        f_out.write(data)


############################################################
## PROCESSING
def toc_sort(item):
    a = None
    b = None
    c = None
    if item.get("generate", {}).get("from") == "endpoint-group-overview":
        a = 0
    else:
        a = 1
    b = item.get("generate", {}).get("endpoint-name", "zz")
    c = item.get("group", "0").lower()
    return a, b, c

def check_toc_group(toc_groups, toc_group_name, toc_group_dir=[], retry=False):
    if toc_group_dir:
        group_data = {"group": toc_group_name, "dir": toc_group_dir}
    else:
        group_data = {"group": toc_group_name, "items": []}
    try:
        entry = next(item for item in toc_groups if item.get("group") == toc_group_name)
        return entry
    except:
        if not retry:
            toc_groups.append(group_data)
            toc_groups.sort(key=toc_sort)
            return check_toc_group(toc_groups, toc_group_name, toc_group_dir, True)
        else:
            print(f"Unable to create TOC entry for {group_data} in {toc_groups}")


def get_tag_data(tag_name):
    try:
        tag_data = next(tag for tag in TAGS if tag.get("name") == tag_name)
        return tag_data
    except:
        print(f"get_tag_info: Missing data for tag name {tag_name}")


def generate_toc():
    for path, properties in PATHS.items():
        for verb in ["get", "post", "put", "delete"]:
            if verb in properties:
                tag_name = properties[verb]["tags"][0]
                tag_data = get_tag_data(tag_name)
                tag_desc = tag_data.get("description")

                operation_id = properties[verb]["operationId"]
                if not operation_id in OPERATION_IDS:
                    OPERATION_IDS.append(operation_id)
                endpoint_group = tag_name

                cat = None
                for main_cat in [
                    "Sites",
                    "Orgs",
                    "MSPs",
                    "Admins",
                    "Installer",
                    "Self",
                    "Samples",
                    "Utilities",
                    "Constants",
                ]:
                    if tag_name.startswith(main_cat):
                        cat = main_cat.lower()
                        tag_name = tag_name.replace(main_cat, "", 1).strip()
                        break
                if not cat:
                    print(f"Missing Main Cat for {tag_name}")

                else:
                    check_toc_group(TOC_API_ITEMS["root"], cat.title(), f"{cat}")
                    if not TOC_API_ITEMS.get(cat):
                        TOC_API_ITEMS[cat] = []

                    toc_group_items = TOC_API_ITEMS[cat]
                    if tag_name:
                        for tag_part in tag_name.split(" - "):
                            tmp = tag_part.strip()
                            toc_group_items = check_toc_group(
                                toc_group_items, tmp, [], False
                            )["items"]
                    ## adding the "overview"
                    try:
                        next(
                            item
                            for item in toc_group_items
                            if item.get("generate", {}).get("from") == "endpoint-group-overview"
                        )
                    except:
                        toc_group_items.append(
                            {"generate": {"from": "endpoint-group-overview", "endpoint-group": endpoint_group}}
                        )
                    ## adding the item
                    toc_group_items.append(
                        {
                            "generate": {
                                "from": "endpoint",
                                "endpoint-name": operation_id,
                                "endpoint-group": endpoint_group,
                            }
                        }
                    )
                    toc_group_items.sort(key=toc_sort)

    for cat, items in TOC_API_ITEMS.items():
        if cat == "root":
            toc_file_path = os.path.abspath(
                os.path.join(os.path.curdir, f"{TOC_FOLDER}")
            )
            if not os.path.isdir(toc_file_path):
                os.makedirs(toc_file_path)
            with open(os.path.join(toc_file_path, "toc.yml"), "w") as toc_out_file:
                yaml.dump({"toc": items}, toc_out_file, indent=2)
            post_processing(os.path.join(toc_file_path, "toc.yml"))

        else:
            toc_file_path = os.path.abspath(
                os.path.join(os.path.curdir, f"{TOC_FOLDER}/{cat}")
            )
            if not os.path.isdir(toc_file_path):
                os.makedirs(toc_file_path)
            with open(os.path.join(toc_file_path, "toc.yml"), "w") as toc_out_file:
                yaml.dump({"toc": items}, toc_out_file, indent=2)
            post_processing(os.path.join(toc_file_path, "toc.yml"))

    # main_toc = [
    #     {
    #         "group": "Getting Started",
    #         "items": [{"from": "getting-started", "generate": "How to Get Started"}],
    #     },
    #     {"group": "Guides", "dir": "guides"},
    #     {"group": "API", "items": [
    #         {"group": "Self", "dir": "/api/self"},
    #         {"group": "Admins", "dir": "/api/admins"},
    #         {"group": "Sites", "dir": "/api/sites"},
    #         {"group": "Orgs", "dir": "/api/orgs"},
    #         {"group": "MSPs", "dir": "/api/msps"},
    #         {"group": "Installer", "dir": "/api/installer"},
    #         {"group": "Utilities", "dir": "/api/utilities"},
    #         {"group": "Constants", "dir": "/api/constants"},
    #         {"group": "Samples", "dir": "/api/samples"},
    #     ]},
    #     {"from": "models", "generate": "Models"},
    # ]
    # toc_file_path = os.path.abspath(os.path.join(os.path.curdir, TOC_FOLDER))
    # with open(os.path.join(toc_file_path, "toc.yml"), "w") as toc_out_file:
    #     yaml.dump({"toc": main_toc}, toc_out_file, ind
    # ent=2)

############################################################
## ENTRY POINT
if os.path.isdir(TOC_FOLDER):
    shutil.rmtree(TOC_FOLDER)
generate_toc()
print(f"#OPERATIONS = {len(OPERATION_IDS)}")
