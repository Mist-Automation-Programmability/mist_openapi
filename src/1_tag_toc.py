import yaml

schemas = {}
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
    "SAMPLES": {},}


OPERATION_IDS = []

for p in PATHS:
    properties = PATHS[p]
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            operation_id = properties[verb]["operationId"]
            tag = ""
            cats = []
            for t in properties[verb]["tags"]:
                if t.startswith("cat:"):
                    cats.append(t.replace("cat:","").split(":"))
                elif not tag:
                    tag = t
                else:
                    print(f"{operation_id}>>{tag}+{t}")
            for cat in cats:
                item = ITEMS
                for c in cat:
                    if not item.get(c):
                        item[c]={}
                    item = item[c]
                    if not operation_id in OPERATION_IDS:
                        OPERATION_IDS.append(operation_id)
                if not item.get(tag):
                    item[tag]=[]
                item[tag].append(operation_id)

def generate(items, group):
    data = [{"generate":{"from":"endpoint-group-overview","endpoint-group": group}}]
    for item in items:
        if isinstance(items[item], dict):
            tmp = generate(items[item], f"{group} {item}")
            data.append({"group":item, "items": tmp})
        elif isinstance(items[item], list):
            tmp = []
            for i in items[item]:
                tmp.append({"generate": {"from":"endpoint", "endpoint-name":i, "endpoint-group": f"{group} {item}"}})
            tmp2=sorted(tmp, key=lambda d: d['generate']['endpoint-name'])
            data +=  tmp2
    return data

OUT = [
    {
        "group":"MANAGEMENT",
        "items":generate(ITEMS["MIST"], "MANAGEMENT")
        },
    {"group":"WI-FI Assurance", "items":generate(ITEMS["WLAN"], "MANAGEMENT")},
    {"group":"LAN Assurance", "items":generate(ITEMS["LAN"], "MANAGEMENT")},
    {"group":"WAN Assurance", "items":generate(ITEMS["WAN"], "MANAGEMENT")},
    {"group":"ACCESS Assurance", "items":generate(ITEMS["NAC"], "MANAGEMENT")},
    {"group":"LOCATION", "items":generate(ITEMS["LOCATION"], "MANAGEMENT")},
    {"group":"SAMPLES", "items":generate(ITEMS["SAMPLES"], "MANAGEMENT")},
]

with open("./content/toc.yml", "w") as toc_out_file:
    yaml.dump(OUT, toc_out_file)


print(f"#OPERATIONS = {len(OPERATION_IDS)}")