""" 
- x-stoplight

[ ]*x-stoplight:
[ ]*id:.*$
-
 """
import yaml

FILENAME="openapi.yaml"

VERBS = ["get", "post", "put", "delete"]
CONTENT_TYPES = ["application/json", "application/xml", "multipart/form-data"]
with open(FILENAME, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)

DELETED = 0

for path in data["paths"]:
    for verb in VERBS:
        if verb in data["paths"][path]:
            path_data = data["paths"][path][verb]
            if "requestBody" in path_data:
                for content_type in CONTENT_TYPES:
                    if path_data["requestBody"].get("content", {}).get(content_type, {}).get("schema", {}).get("x-examples"):
                        print(f"Response {path} - {verb}")
                        del path_data["requestBody"]["content"][content_type]["schema"]["x-examples"]
                        DELETED += 1
            if "responses" in path_data:
                for response in path_data["responses"]:
                    if path_data["responses"][response].get("content", {}).get("application/json", {}).get("schema", {}).get("x-examples"):
                        print(f"Response {path} - {verb}")
                        del path_data["responses"][response]["content"]["application/json"]["schema"]["x-examples"]
                        DELETED += 1

for response in data["components"].get("responses", {}):
    response_data = data["components"]["responses"][response]
    if response_data.get("content", {}).get("application/json", {}).get("schema", {}).get("x-examples"):
        print(f"Response - {response}")
        del response_data["content"]["application/json"]["schema"]["x-examples"]
        DELETED += 1

for schema in data["components"].get("schemas", {}):
    schema_data = data["components"]["schemas"][schema]
    if schema_data.get("x-examples"):
        print(f"Schema - {schema}")
        del schema_data["x-examples"]
        DELETED += 1

with open (FILENAME, "w") as f:
    yaml.dump({"openapi": data["openapi"]}, f)
    yaml.dump({"info": data["info"]}, f)
    yaml.dump({"servers": data["servers"]}, f)
    yaml.dump({"security": data["security"]}, f)
    yaml.dump({"tags": data["tags"]}, f)
    yaml.dump({"paths": data["paths"]}, f)
    yaml.dump({"components": data["components"]}, f)

print(DELETED)