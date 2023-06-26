import yaml
import re
import json
schemas = {}
paths = {}

with open("mist.openapi.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


cat = [ "Constants", "Authentication", "Monitor", "Operational", "Installer"]
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
    "operational": {},
    "installer": {},
}

cat_params = {
    "constants": [],
    "authentication": [],
    "monitor": [],
    "operational": [],
    "installer": [],
    "installer": [],
}
cat_responses = {
    "constants": [],
    "authentication": [],
    "monitor": [],
    "operational": [],
    "installer": [],
}

cat_schemas = {
    "constants": [],
    "authentication": [],
    "monitor": [],
    "operational": [],
    "installer": [],
}

missing = []

def add_endpoint(category:str, path:str, parameters:dict, verb:str, endpoint:dict):
    if not path in cat_paths[category]:
        if parameters:
            for parameter in parameters:
                if "$ref" in parameter:
                    ref = parameter["$ref"].split("/")[-1:][0]
                    if not ref in cat_params[category]: cat_params[category].append(ref)
            cat_paths[category][path] = {"parameters": parameters}
        else:
            cat_paths[category][path] = {}

    endpoint_str = str(endpoint)

    re_schema = "\$ref'*: '#/components/schemas/([0-9a-zA-Z_.-]+)'"
    for entry in re.findall(re_schema, endpoint_str):
        if not entry in cat_schemas[category]: cat_schemas[category].append(entry)

    re_parameters = "\$ref'*: '#/components/parameters/([0-9a-zA-Z_.-]+)'"
    for entry in re.findall(re_parameters, endpoint_str):
        if not entry in cat_params[category]: cat_params[category].append(entry)

    re_responses = "\$ref'*: '#/components/responses/([0-9a-zA-Z._-]+)'"
    for entry in re.findall(re_responses, endpoint_str):
        if not entry in cat_responses[category]: cat_responses[category].append(entry)

    cat_paths[category][path][verb] = endpoint


def split():
    for path in parts["paths"]:
        properties = parts["paths"][path]
        parameters = properties.get("parameters")
        for verb in properties:
            if verb in verbs:
                if path.startswith("/api/v1/installer/"):
                    add_endpoint("installer", path, parameters, verb, properties[verb])
                elif "Constants" in properties[verb]["tags"]:
                    add_endpoint("constants", path, parameters, verb, properties[verb])
                elif "Authentication" in properties[verb]["tags"]:
                    add_endpoint("authentication", path, parameters, verb, properties[verb])
                elif "Monitor" in properties[verb]["tags"]:
                    add_endpoint("monitor", path, parameters, verb, properties[verb])
                elif "Operational" in properties[verb]["tags"]:
                    add_endpoint("operational", path, parameters, verb, properties[verb])
                else:
                    missing.append(f"{path} >> {properties[verb]['operationId']}")

    for miss in missing:
        print(miss)



def get_schemas(src_schemas, schemas):    
    re_schema = "\$ref'*: '#/components/schemas/([0-9a-zA-Z_.-]+)'"
    dst_schemas = {}
    for schemas_def in schemas:
            dst_schemas[schemas_def] = src_schemas[schemas_def]
            schema_str = str(src_schemas[schemas_def])
            sub_schemas = re.findall(re_schema, schema_str)
            tmp = get_schemas(src_schemas, sub_schemas)
            for entry in tmp:
                dst_schemas[entry] = tmp[entry]
    #if dst_parameters: components["schemas"] = dst_schemas
    return dst_schemas

def save():
    for category in cat_paths:    
        filename = f"../v2/mist.openapi.{category}.yml"
        components = {}
        additional_schemas = []

        src_parameters = parts.get("components", {}).get("parameters")
        dst_parameters = {}
        for param in src_parameters:
            if param in cat_params[category]:
                dst_parameters[param] = src_parameters[param]
        if dst_parameters: components["parameters"] = dst_parameters

        src_responses = parts.get("components", {}).get("responses")    
        dst_responses = {}
        for response_def in cat_responses[category]:
            dst_responses[response_def] = src_responses[response_def]
            response_str = str(src_responses[response_def])
            re_responses = "\$ref'*: '#/components/schemas/([a-zA-Z_.-]+)'"
            for entry in re.findall(re_responses, response_str):
                if not entry in additional_schemas: additional_schemas.append(entry)

        if dst_parameters: components["responses"] = dst_responses

        schemas = cat_schemas[category] + additional_schemas
        dst_schemas = get_schemas(parts.get("components", {}).get("schemas"), schemas)
        if dst_parameters: components["schemas"] = dst_schemas

        data = {
            "openapi" : parts.get("openapi"),
            "info" : parts.get("info"),
            "servers" : parts.get("servers"),
            "security" : parts.get("security"),
            "tags" : parts.get("tags"),
            "paths" : cat_paths.get(category),
            "components" : components,
            "x-tagGroups" : parts.get("x-tagGroups"),
        }    


        output_str = json.dumps(data)
        re_schema = "\$ref\"*: \"#/components/schemas/([0-9a-zA-Z_.-]+)\""
        for entry in re.findall(re_schema, output_str):
            output_str = re.sub(re_schema, f"$ref\": \"./components/schemas/{entry}.yaml\"", output_str)
        data = json.loads(output_str)

        with open(filename, 'w') as oas_out_file:
            for item in order:
                yaml.dump({item: data[item]}, oas_out_file)


if __name__ == "__main__":
    split()
    save()                