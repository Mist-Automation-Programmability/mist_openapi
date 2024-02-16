import yaml
import re
import json

with open("./mist.openapi_grp3.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths")


ITEMS = {
    "MIST": {},
    "WLAN": {},
    "LAN": {},
    "WAN": {},
    "NAC": {},
    "LOCATION": {},
    "SAMPLES": {},
    "COMMON": {},
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

for p in PATHS:
    properties = PATHS[p]
    operations = {}
    others = {}
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            operations[verb] = properties[verb]
        else:
            others[verb] = properties[verb]

    for verb, operation in operations.items():
        operation_id = properties[verb]["operationId"]
        cats = []
        for t in properties[verb]["tags"]:
            if t.startswith("cat:"):
                cat = t.replace("cat:","").split(":")[0]
                if not cat in cats:
                    cats.append(cat)
        if len(cats) == 1:
            cat = cats[0]
            if not p in ITEMS[cat]:
                ITEMS[cat][p]=others
            ITEMS[cat][p][verb] = operation
        else:
            cat = "COMMON"
            if not p in ITEMS[cat]:
                ITEMS[cat][p]=others
            ITEMS[cat][p][verb] = operation


REG = r"\"#\/components\/(?P<t>[^\/]*)\/(?P<n>[^\"]*)\""

for cat, operations in ITEMS.items():
    file = f"./spec/mist.openapi.{cat.lower()}.yml"
    components = data["components"]
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
                        components[rtype][rname] = {"$ref": f"./components/{rtype}/{rname}.yml"}
            elif item == "components":
                yaml.dump({item: components}, oas_out_file)
            else:
                yaml.dump({item: data[item]}, oas_out_file)
