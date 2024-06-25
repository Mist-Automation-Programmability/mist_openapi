""" 
- add x-logo and x-tagGroups to OpenApi Spec
- only required for readocly portal 
"""

import yaml
import json
import re

FILE_IN = "./mist.openapi.yml"
FILE_OUT_YAML = "../mist.openapi.yml"
FILE_OUT_JSON = "../mist.openapi.json"
LOGO = {
    "altText": "Juniper-MistAI",
    "backgroundColor": "#FFFFFF",
    "url": "https://www.mist.com/wp-content/uploads/logo.png",
}
GROUPS = [
    {"name": "Admins", "tags": []},
    {"name": "Self","tags": []},
    {"name": "Sites","tags": []},
    {"name": "Orgs","tags": []},
    {"name": "MSPs","tags": []},
    {"name": "Utilities","tags": []},
    {"name": "Installer", "tags": []},
    {"name": "Samples", "tags": []},
    {"name": "Constants","tags": []},
]

PATHS = {}
TAGS = []


def register_tags():
    global GROUPS
    verbs = ["get", "post", "put", "delete"]
    out = {}
    for group in GROUPS:
        out[group["name"]]=[]
    for path, data in PATHS.items():
        for verb, opereration in data.items():
            if verb in verbs:
                tag = opereration["tags"][0]
                cat = tag.split(" ")[0].strip()
                if cat in out:
                    if not tag in out[cat]:
                        if not next(item for item in TAGS if item["name"] == tag):
                            print(f"MISSING TAG: {tag}")
                        out[cat].append(tag)
                else:
                    print(f"Missing tag group for {tag}")
    for group in GROUPS:
        out[group["name"]].sort()
        group["tags"]= out[group["name"]]

    # check for unused tag
    for tag in TAGS:
        used = False
        for group in GROUPS:
            if tag["name"] in group["tags"]:
                used = True
        if not used:
            print(f"UNUSED TAG: {tag}")
        

with open(FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths", {})
    TAGS = data.get("tags", [])

register_tags()
data["info"]["x-logo"] = LOGO

### update links
data_str = json.dumps(data, indent=4, default=str)
LINK_RE = r"\$e/[^^/]*/"
data_str=re.sub(LINK_RE, "/#operations/", data_str)
data = json.loads(data_str)

with open(FILE_OUT_YAML, "w") as f:
    yaml.dump({"openapi": data["openapi"]}, f)
    yaml.dump({"info": data["info"]}, f)
    yaml.dump({"servers": data["servers"]}, f)
    yaml.dump({"security": data["security"]}, f)
    yaml.dump({"tags": data["tags"]}, f)
    yaml.dump({"paths": data["paths"]}, f)
    yaml.dump({"components": data["components"]}, f)
    yaml.dump({"x-tagGroups": GROUPS}, f)


with open(FILE_OUT_JSON, "w") as oas_out_file:
    json.dump(data, oas_out_file)