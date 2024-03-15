"""
This script is generating the toc files from the main openapi spec (single file) based on the documentation tag
Can be filtered to one or multiple spec files based on the .filters file
"""
import re
import os
import sys
import yaml

TOC_FILE_IN = "../src/src_toc.yml"
TOC_FILE_OUT = "../src/content/toc.yml"
SPEC_FOLDER = "../src./spec/"
TOC_FOLDER = "../src/content/api/"
FILTER_FILE = "./.filters"
PRE_TAG="op"


with open(FILTER_FILE, "r") as filter_file:
    filters_string = filter_file.read().split("=")[1].split("#")[0]
    FILTER = filters_string.split(",")

OPERATION_IDS = []


def add_endpoint(
        items: list,
        operation_id: str,
        endpoint_group: str,
        groups: list,
        level: int = 0,
        retry: int = 0
    ):
    """
    return destination group where the endpoint must be documented
    if the group (or group path) doesn't exist, create it
    """
    current_group = groups[level : level + 1][0]
    group_name = f"tag:{':'.join(groups[:level+1])}"
    if level > 5:
        print(f"too many levels for {groups}, {group_name}")
        sys.exit(0)
    next_groups = groups[level + 1 :]
    next_items = None
    ##
    print(f"{operation_id}".ljust(80, "-"))
    print(items)
    print(endpoint_group)
    print(groups)
    print(current_group)
    ##
    if retry >= 5:
        print(f"unable to create the group entry for {groups}, {group_name}")
        sys.exit(0)
    else:
        try:
            next_items = next(item for item in items if item.get("group", "").lower() == current_group.lower())
        except:
            # if len(next_groups) == 0:
            #     group_title = current_group
            # else:
            group_title = current_group.title()
            items.append({"group": group_title, "items": []})
            items.sort(key=lambda item: item.get("group", "0"))
            next_items = next(item for item in items if item.get("group", "").lower() == current_group.lower())
        finally:
            if next_groups:
                add_endpoint(next_items["items"], operation_id, endpoint_group, groups, level + 1)
            else:
                if next_items and len(next_items) == 0:
                    next_items["items"] = [
                        {
                            "generate": {
                                "endpoint-group": f"{PRE_TAG}:{':'.join(groups)}",
                                "from": "endpoint-group-overview",
                            }
                        }
                    ]
                next_items["items"].append(
                    {
                        "generate": {
                            "from": "endpoint",
                            "endpoint-name": operation_id,
                            "endpoint-group": endpoint_group,
                        }
                    }
                )
                next_items["items"].sort(
                    key=lambda item: item.get("generate", {}).get("endpoint-name", "0")
                )


def process_spec_file(spec_data: dict, items: list):
    """
    process the spec file
    add each endpoint into the toc based on the group path
    """
    for path, properties in spec_data.get("paths", {}).items():
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                operation_id = properties[verb]["operationId"]
                tag = ""
                groups = []
                endpoint_group = ""
                category = ""
                for t in properties[verb]["tags"]:
                    if t.startswith(f"{PRE_TAG}:"):
                        if not groups:
                            endpoint_group = t
                            category = t.split(":")[1:2][0]
                            groups = t.split(":")[2:]
                        else:
                            print(f"operationid {operation_id} has too many groups")
                    elif not tag:
                        tag = t
                    else:
                        print(f"operationid {operation_id} has too many tags")
                        
                if groups and category == groups[-1:]:
                    groups = groups[:-1]
                if not FILTER or category in FILTER:
                    if not operation_id in OPERATION_IDS:
                        OPERATION_IDS.append(operation_id)
                        add_endpoint(items, operation_id, endpoint_group, groups)
                    else:
                        print(f"operationid {operation_id} listed more than one time")


############################################################
## POST PROCESSING
def post_procerssing(file_path):
    re_one = r"([ ]*)- generate:\n([ ]*)  (endpoint-group: .*)\n([ ]*)  (from: .*)"
    re_two = r"([ ]*)- generate:\n([ ]*)  (endpoint-group: .*)\n([ ]*)  (endpoint-name: .*)\n([ ]*)  (from: .*)"
    with open(file_path, "r") as f_in:
        data = f_in.read()

    data = re.sub(re_one, "\\1- generate:\n\\2\\3\n\\4\\5", data)
    data = re.sub(re_two, "\\1- generate:\n\\2\\3\n\\4\\5\n\\6\\7", data)
    with open(file_path, "w") as f_out:
        f_out.write(data)


def generate_toc():
    for folder in os.listdir(SPEC_FOLDER):
        items = []
        spec_folder_path = os.path.join(SPEC_FOLDER, folder)
        toc_folder_path = os.path.join(TOC_FOLDER, folder)

        if os.path.isdir(spec_folder_path):
            for file in os.listdir(spec_folder_path):
                spec_file_path = os.path.join(spec_folder_path, file)
                toc_file_path = os.path.join(toc_folder_path, "toc.yml")
                if os.path.isfile(spec_file_path) and spec_file_path.endswith(".yml"):
                    with open(spec_file_path, "r") as spec_file_data:
                        spec_data = yaml.load(
                            spec_file_data, Loader=yaml.loader.SafeLoader
                        )
                        process_spec_file(spec_data, items)
                    with open(toc_file_path, "w") as toc_out_file:
                        yaml.dump({"toc": items}, toc_out_file, indent=2)
                    post_procerssing(toc_file_path)


generate_toc()
print(f"#OPERATIONS = {len(OPERATION_IDS)}")
