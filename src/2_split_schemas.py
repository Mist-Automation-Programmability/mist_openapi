import yaml
import re
import json
schemas = {}
paths = {}
with open("mist.openapi.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


cat = [ "Constants", "Authentication", "Monitor", "Configuration"]
verbs = ["get", "post", "put", "delete"]
order = ["openapi", "info", "servers", "security",
         "tags", "paths", "components", "x-tagGroups"]

parts = {
    "openapi" : data.get("openapi"),
    "info" : data.get("info"),
    "servers" : data.get("servers"),
    "security" : data.get("security"),
    "tags" : data.get("tags"),
    "paths" : data.get("paths"),
    "components" : data.get("components"),
    "x-tagGroups" : data.get("x-tagGroups"),
}

cat_paths = {
    "constants": {},
    "authentication": {},
    "monitor": {},
    "configuration": {},
}

cat_params = {
    "constants": [],
    "authentication": [],
    "monitor": [],
    "configuration": [],
}
cat_responses = {
    "constants": [],
    "authentication": [],
    "monitor": [],
    "configuration": [],
}

cat_schemas = {
    "constants": [],
    "authentication": [],
    "monitor": [],
    "configuration": [],
}

missing = []


def create_schema(title:str, schema_data:dict):
    output = {
        "title":title
    }
    for key in schema_data:
        output[key]=schema_data[key]
    output_str = json.dumps(output)
    re_schema = "\$ref\"*: \"#/components/schemas/([0-9a-zA-Z_.-]+)\""
    for entry in re.findall(re_schema, output_str):
        output_str = re.sub(re_schema, f"$ref\": \"./{entry}.yaml\"", output_str)
    output = json.loads(output_str)
    
    with open(f"../v2/components/schemas/{title}.yaml", "w") as f:
        yaml.dump(output, f)


for schema_title in parts["components"].get("schemas"):
    create_schema(schema_title, parts["components"]["schemas"][schema_title])