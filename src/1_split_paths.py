import yaml
import re
import json
schemas = {}
paths = {}

with open("mist.openapi.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


cat = [ "Constants", "Authentication", "Monitor", "Configuration", "Installer"]
verbs = ["get", "post", "put", "delete"]
order = ["openapi", "info", "servers", "security",
         "tags", "paths", "components"]

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
    "monitor": {
        "msps": {},
        "orgs": {},
        "sites": {},
        "admins": {}
    },
    "configuration": {
        "msps": {},
        "orgs": {},
        "sites": {},
        "admins": {}
    },
    "installer": {},
    "webhook": {},
}

cat_params = {
    "constants": [],
    "authentication": [],
    "monitor": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "configuration": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "installer": [],
    "webhook": [],
}
cat_responses = {
    "constants": [],
    "authentication": [],
    "monitor": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "configuration": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "installer": [],
    "webhook": [],
}

cat_schemas = {
    "constants": [],
    "authentication": [],
    "monitor": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "configuration": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "installer": [],
    "webhook": [],
}

cat_tags = {
    "constants": [],
    "authentication": [],
    "monitor": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "configuration": {
        "msps": [],
        "orgs": [],
        "sites": [],
        "admins": []
    },
    "installer": [],
    "webhook": [],
}

endpoints_count = {
    "get": 0,
    "post": 0,
    "put": 0,
    "delete": 0
}

missing = []

def add_endpoint(category:str, path:str, parameters:dict, verb:str, endpoint:dict, scope:str=None):
    if scope: 
        cat_path = cat_paths[category][scope]
        cat_schema = cat_schemas[category][scope]
        cat_param = cat_params[category][scope]
        cat_response = cat_responses[category][scope]
        cat_tag = cat_tags[category][scope]
    else:
        cat_path = cat_paths[category]
        cat_schema = cat_schemas[category]
        cat_param = cat_params[category]
        cat_response = cat_responses[category]
        cat_tag = cat_tags[category]
    if not path in cat_path:
        if parameters:
            for parameter in parameters:
                if "$ref" in parameter:
                    ref = parameter["$ref"].split("/")[-1:][0]
                    if not ref in cat_param:cat_param.append(ref)
            cat_path[path] = {"parameters": parameters}
        else:
            cat_path[path] = {}

    endpoint_str = str(endpoint)

    re_schema = "\$ref'*: '#/components/schemas/([0-9a-zA-Z_.-]+)'"
    for entry in re.findall(re_schema, endpoint_str):
        if not entry in cat_schema: cat_schema.append(entry)

    re_parameters = "\$ref'*: '#/components/parameters/([0-9a-zA-Z_.-]+)'"
    for entry in re.findall(re_parameters, endpoint_str):
        if not entry in cat_param: cat_param.append(entry)

    re_responses = "\$ref'*: '#/components/responses/([0-9a-zA-Z._-]+)'"
    for entry in re.findall(re_responses, endpoint_str):
        if not entry in cat_response: cat_response.append(entry)

    for tag in endpoint.get("tags",[]):
        if not tag in cat_tag: cat_tag.append(tag)


    cat_path[path][verb] = endpoint


def select_scope(endpoint:dict):
    if endpoint.get("operationId") in ["verifyAdminInvite", "activateSdkInvite", "registerNewAdmin", "verifyRegistration"]:
        return "orgs"
    elif endpoint.get("operationId") in ["testSiteWlanTelstraSetup", "testSiteWlanTwilioSetup"]:
        return "sites"
    else:
        print(endpoint.get("operationId"))
        while True:
            print("1) msps")
            print("2) orgs")
            print("3) sites")
            print("4) admins")
            resp = input("scope? ")
            if resp == "1":
                return "msps"
            elif resp == "2":
                return "orgs"
            elif resp == "3":
                return "sites"
            elif resp == "4":
                return "admins"

def split_scope(category:str, path:str, parameters:dict, verb:str, endpoint:dict):
    scope = path.split("/")[3]
    if  scope in ["msps", "orgs", "sites"]:
        add_endpoint(category, path, parameters, verb, endpoint, path.split("/")[3])
    elif  scope == "self":
        add_endpoint(category, path, parameters, verb, endpoint, "admins")
    else:
        scope = select_scope(endpoint)
        add_endpoint(category, path, parameters, verb, endpoint, scope)
    
   
def split():
    for path in parts["paths"]:
        properties = parts["paths"][path]
        parameters = properties.get("parameters")
        for verb in properties:
            if verb in verbs:
                endpoints_count[verb]+=1
                print(f'>>>>>>>>>>>>>>>>>>>>>{verb} {path}')
                if path.startswith("/api/v1/installer/"):
                    add_endpoint("installer", path, parameters, verb, properties[verb])
                elif path.startswith("/webhook_example/"):
                    add_endpoint("webhook", path, parameters, verb, properties[verb])
                elif "Constants" in properties[verb]["tags"]:
                    add_endpoint("constants", path, parameters, verb, properties[verb])
                elif "Authentication" in properties[verb]["tags"]:
                    add_endpoint("authentication", path, parameters, verb, properties[verb])
                elif "Monitor" in properties[verb]["tags"]:
                    split_scope("monitor", path, parameters, verb, properties[verb])
                elif "Configuration" in properties[verb]["tags"]:
                    split_scope("configuration", path, parameters, verb, properties[verb])
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

def save_file(filename:str, cat_path:dict, cat_schema: dict, cat_param:list, cat_response:list, cat_tag:list):  
        components = {}
        additional_schemas = []

        src_parameters = parts.get("components", {}).get("parameters")
        dst_parameters = {}
        for param in src_parameters:
            if param in cat_param:
                dst_parameters[param] = src_parameters[param]
        if dst_parameters: components["parameters"] = dst_parameters

        src_responses = parts.get("components", {}).get("responses")    
        dst_responses = {}
        for response_def in cat_response:
            dst_responses[response_def] = src_responses[response_def]
            response_str = str(src_responses[response_def])
            re_responses = "\$ref'*: '#/components/schemas/([a-zA-Z_.-]+)'"
            for entry in re.findall(re_responses, response_str):
                if not entry in additional_schemas: additional_schemas.append(entry)

        if dst_parameters: components["responses"] = dst_responses

        schemas = cat_schema + additional_schemas
        dst_schemas = get_schemas(parts.get("components", {}).get("schemas"), schemas)
        if dst_parameters: components["schemas"] = dst_schemas

        tags = []
        for tag in parts.get("tags"):
            if tag.get("name") in cat_tag:
                tags.append(tag)

        data = {
            "openapi" : parts.get("openapi"),
            "info" : parts.get("info"),
            "servers" : parts.get("servers"),
            "security" : parts.get("security"),
            "tags" : tags,
            "paths" : cat_path,
            "components" : {
                "parameters": dst_parameters,
                "responses": dst_responses
            }
        }    


        output_str = json.dumps(data)
        re_schema = "\$ref\"*: \"#/components/schemas/([0-9a-zA-Z_.-]+)\""
        for entry in re.findall(re_schema, output_str):
            tmp_re_schema = f"\$ref\"*: \"#/components/schemas/{entry}\""
            output_str = re.sub(tmp_re_schema, f"$ref\": \"./components/schemas/{entry}.yaml\"", output_str)
        data = json.loads(output_str)

        with open(filename, 'w') as oas_out_file:
            for item in order:
                yaml.dump({item: data[item]}, oas_out_file)


def save():
    for category in cat_paths:  
        if category in ["monitor", "configuration"]:
            for scope in cat_paths[category]:
                cat_path = cat_paths[category][scope]
                cat_schema = cat_schemas[category][scope]
                cat_param = cat_params[category][scope]
                cat_response = cat_responses[category][scope]
                cat_tag = cat_tags[category][scope]
                filename = f"../v2/mist.openapi.{category}.{scope}.yml"
                save_file(filename, cat_path, cat_schema, cat_param, cat_response, cat_tag)
        else:
            cat_path = cat_paths[category]
            cat_schema = cat_schemas[category]
            cat_param = cat_params[category]
            cat_response = cat_responses[category]
            cat_tag = cat_tags[category]
            filename = f"../v2/mist.openapi.{category}.yml"
            save_file(filename, cat_path, cat_schema, cat_param, cat_response, cat_tag)




if __name__ == "__main__":
    split()
    save()        
    print("".center(80, "-"))
    print(f"GET   : {endpoints_count['get']}")
    print(f"POST  : {endpoints_count['post']}")
    print(f"PUT   : {endpoints_count['put']}")
    print(f"DELETE: {endpoints_count['delete']}")
    print()
    print(f"TOTAL : {endpoints_count['get'] + endpoints_count['post'] +endpoints_count['put'] +endpoints_count['delete'] }")