import yaml

SPEC_FILE = "./openapi.yaml"
EXCEPTIONS = [
    "privilege_self_views",
    "privilege_org_views",
    "privilege_msp_view",
    "admin_privilege_view",
]

with open(SPEC_FILE, "r") as f_in:
    data = yaml.load(f_in, Loader=yaml.loader.SafeLoader)


schemas = data.get("components", {}).get("schemas")
for n, s in schemas.items():
    if n not in EXCEPTIONS:
        if s.get("enum"):
            enum_desc = []
            e = s["enum"]
            e = e.sort()
            for v in s.get("enum"):
                enum_desc.append(f"`{v}`")
            new_desc = f"enum: {', '.join(enum_desc)}"
            if not s.get("description"):
                s["description"] = new_desc
            elif not "enum: " in s["description"] and not "enum:\n" in s["description"]:
                s["description"] += ". " + new_desc

data["components"]["schemas"] = schemas

with open(SPEC_FILE, "w") as f:
    yaml.dump({"openapi": data["openapi"]}, f)
    yaml.dump({"info": data["info"]}, f)
    yaml.dump({"servers": data["servers"]}, f)
    yaml.dump({"security": data["security"]}, f)
    yaml.dump({"tags": data["tags"]}, f)
    yaml.dump({"paths": data["paths"]}, f)
    yaml.dump({"components": data["components"]}, f)
