import yaml

schemas = {}
with open("./mist.openapi_grp2.yml", "r") as f:
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
            cat_1 = []
            cat_2 = []
            new_tags = []
            for t in properties[verb]["tags"]:
                if t.startswith("cat1:"):
                    cat_1.append(t.replace("cat1:", ""))
                elif t.startswith("cat2:"):
                    cat_2.append(t.replace("cat2:", ""))
                else:
                    new_tags.append(t)
            if not cat_1:
                print(f"{operation_id} >> missing cat1")
            elif not cat_2:
                for c1 in cat_1:
                    new_tags.append(f"cat:{c1}")
                properties[verb]["tags"] = new_tags
            else:
                for c1 in cat_1:
                    for c2 in cat_2:
                        new_tags.append(f"cat:{c1}:{c2}")
                properties[verb]["tags"] = new_tags


with open("mist.openapi_grp3.yml", "w") as oas_out_file:
    for item in ORDER:
        yaml.dump({item: data[item]}, oas_out_file)
