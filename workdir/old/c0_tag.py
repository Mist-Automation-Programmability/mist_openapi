"""
This script is parsing the main openapi spec (single file) and add the category tag to each
endpoint based on the path
"""
import yaml

SPEC_FILE_IN="./mist.openapi.yml"
SPEC_FILE_OUT="../tmp/mist.openapi_grp1.yml"


with open(SPEC_FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths")

OPERATION_IDS = []
VERBS = ["get", "post", "put", "delete"]
ORDER = [
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components"
]

NEW_TAGS = []

def _set_tag(path):
    properties = data["paths"][path]
    operation_tag = ".".join(path.split("/"))[1:]
    if operation_tag not in NEW_TAGS:
        NEW_TAGS.append(operation_tag)
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            operation_id = properties[verb]["operationId"]
            if not operation_id in OPERATION_IDS:
                OPERATION_IDS.append(operation_id)
            properties[verb]["tags"].insert(0, operation_tag)
            

for path in PATHS:
    _set_tag(path)

for tag in NEW_TAGS:
    data["tags"].append({"name": tag})
with open(SPEC_FILE_OUT, "w") as oas_out_file:
    for item in ORDER:
        yaml.dump({item: data[item]}, oas_out_file)

print(f"#OPERATIONS = {len(OPERATION_IDS)}")
