""" 
- x-stoplight

[ ]*x-stoplight:
[ ]*id:.*$
-
 """
import yaml

paths = {}
verbs = ["get", "post", "put", "delete"]
content_types = ["application/json", "application/xml", "multipart/form-data"]
with open("mist.openapi.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)

deleted = 0

for path in data["paths"]:
    for verb in verbs:
        if verb in data["paths"][path]:
            path_data = data["paths"][path][verb]
            if "requestBody" in path_data:
                for content_type in content_types:
                    if path_data["requestBody"].get("content", {}).get(content_type, {}).get("schema", {}).get("x-examples"):
                        print(f"Response {path} - {verb}")
                        del path_data["requestBody"]["content"][content_type]["schema"]["x-examples"]
                        deleted += 1
            if "responses" in path_data:
                for response in path_data["responses"]:
                    if path_data["responses"][response].get("content", {}).get("application/json", {}).get("schema", {}).get("x-examples"):
                        print(f"Response {path} - {verb}")
                        del path_data["responses"][response]["content"]["application/json"]["schema"]["x-examples"]
                        deleted += 1

for response in data["components"].get("responses", {}):
    response_data = data["components"]["responses"][response]
    if response_data.get("content", {}).get("application/json", {}).get("schema", {}).get("x-examples"):
        print(f"Response - {response}")
        del response_data["content"]["application/json"]["schema"]["x-examples"]
        deleted += 1

for schema in data["components"].get("schemas", {}):
    schema_data = data["components"]["schemas"][schema]
    if schema_data.get("x-examples"):
        print(f"Schema - {schema}")
        del schema_data["x-examples"]
        deleted += 1

with open ("mist.openapi.yml", "w") as f:
    yaml.dump({"openapi": data["openapi"]}, f)
    yaml.dump({"info": data["info"]}, f)
    yaml.dump({"servers": data["servers"]}, f)
    yaml.dump({"security": data["security"]}, f)
    yaml.dump({"tags": data["tags"]}, f)
    yaml.dump({"paths": data["paths"]}, f)
    yaml.dump({"components": data["components"]}, f)
    yaml.dump({"x-tagGroups": data["x-tagGroups"]}, f)

print(deleted)