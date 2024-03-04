"""
This script is parsing the main openapi spec (single file) and generate the documentation tag
(tag:<category>:<type>:<tag>) for each action
"""
import yaml


SPEC_FILE_IN="./tmp/mist.openapi_grp2.yml"
SPEC_FILE_OUT="./tmp/mist.openapi_grp3.yml"
PRE_TAG="op"
with open(SPEC_FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths")


ORDER = [
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components",
    "x-tagGroups",
]


for p in PATHS:
    properties = PATHS[p]
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            operation_id = properties[verb]["operationId"]
            tag_1 = []
            tag_2 = []
            tag_3 = []
            tag_x = []
            new_tags = [PRE_TAG]
            for t in properties[verb]["tags"]:
                if t.startswith("tag1:"):
                    tag_1.append(t.replace("tag1:", ""))
                elif t.startswith("tag2:"):
                    tag_2.append(t.replace("tag2:", ""))
                else:
                    tag_x.append(t)
            if len(tag_1) != 1:
                print(f"{operation_id} >> has {len(tag_1)} tag_1: {tag_1}")
            if len(tag_2) > 1:
                print(f"{operation_id} >> has {len(tag_2)} tag_1: {tag_2}")
            if len(tag_x) != 1:
                print(f"{operation_id} >> has {len(tag_x)} tag_1: {tag_x}")

            if tag_1[0].lower() == "xonstants":
                new_tags = tag_x
            else:
                if tag_x[0].split(" ")[0] in ["Orgs", "Sites", "Msps", "Utilities", "Constants"]:
                    pre = tag_x[0].split(" ")[0]
                    post = " ".join(tag_x[0].split(" ")[1:])
                    if pre not in ["Utilities", "Constants"] and post:
                        tag_3.append(pre)
                        tag_3.append(post)
                    elif post:
                        tag_3.append(post)
                    else:
                        tag_3.append(pre)
                else:
                    tag_3 = tag_x

                t1 = tag_1[0]
                t3 = ":".join(tag_3)
                if not tag_2:
                    new_tags += [t1, t3]
                else:
                    t2 = tag_2[0]
                    if t3.lower() == t2.lower() or not t3:
                        new_tags += [t1, t2]
                    else:
                        new_tags += [t1, t2, t3]
            properties[verb]["tags"] = [":".join(new_tags), tag_x[0]]



with open(SPEC_FILE_OUT, "w") as oas_out_file:
    for item in ORDER:
        yaml.dump({item: data[item]}, oas_out_file)
