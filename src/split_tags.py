import yaml
import re
schemas = {}
paths = {}
with open("src_mist.openapi.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


cat = [ "Constants", "Authentication", "Monitor", "Operational"]
verbs = ["get", "post", "put", "delete"]
order = ["openapi", "info", "servers", "security",
         "tags", "paths", "components", "x-tagGroups"]


for i in schemas:
    data = schemas[i]
    model = {
        "title": i,
        "type": data.get("type"),       
    }
    if data.get("items"): model["items"] = data.get("items")
    if data.get("properties"): model["properties"] = data.get("properties")
    if data.get("description"): model["description"] = data.get("description")
    if data.get("required"): model["required"] = data.get("required")

logs = []
def ask_tag():
    while True:
        print("1) Authentication")
        print("2) Monitor")
        print("3) Operational")
        print("4) Installer")
        resp = input("tags? ")
        if resp == "1": return "Authentication"
        if resp == "2": return "Monitor"
        if resp == "3": return "Operational"
        if resp == "3": return "Installer"

for path in data.get("paths", {}) :
    print(path)
    properties = data["paths"][path]
    if path.startswith("/api/v1/installer/"):
        for verb in properties:  
            if verb in ["get", "post", "put", "delete"]:
                print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")          
                properties[verb]["tags"].append("Installer")
                logs.append(f"{properties[verb]['operationId']} >>>> Operation")
    elif "post" in properties and properties["post"]["operationId"].startswith("create"):
        for verb in properties:  
            if verb in ["get", "post", "put", "delete"]:
                print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")          
                properties[verb]["tags"].append("Operational")
                logs.append(f"{properties[verb]['operationId']} >>>> Operation")
    elif "delete" in properties and properties["delete"]["operationId"].startswith("delete"):
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                logs.append(f"{properties[verb]['operationId']} >>>> Operation")
                properties[verb]["tags"].append("Operational")
    else:
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                if not "Constants" in properties[verb]["tags"]:
                    if properties[verb]["operationId"].startswith("count") or properties[verb]["operationId"].startswith("search") or "Stats" in properties[verb]["operationId"]:
                        logs.append(f"{properties[verb]['operationId']} >>>> Monitor")
                        properties[verb]["tags"].append("Monitor")
                    else:
                        new_tag = ask_tag()
                        if not new_tag in properties[verb]["tags"]:
                            logs.append(f"{properties[verb]['operationId']} >>>> {new_tag}")
                            properties[verb]["tags"].append(new_tag)


with open("mist.openapi.yml", 'w') as oas_out_file:
    for item in order:
        yaml.dump({item: data[item]}, oas_out_file)

with open("./script.log", "w") as f:
    f.write('\n'.join(logs))
