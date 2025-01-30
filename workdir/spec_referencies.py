import yaml
import json
import re

SPEC_FILE="./mist.openapi.yml"
REF_FILE="./spec_referencies.yml"
R = r'"\$ref": "([^"]*)"'

def _check_refs( comp:dict):
    data = {}
    
    string = json.dumps(comp, default=str)
    # #/components/responses/OK
    # #/components/schemas/rf_client_type
    components = re.findall(R, string)
    for c in components:
        c_splitted = c.split("/")
        if len(c_splitted) == 4:
            c_type = c_splitted[2]
            c_name = c_splitted[3]
            data[c_name] = _check_refs( DATA.get("components", {}).get(c_type, {}).get(c_name))
    return data


with open(SPEC_FILE, "r") as f:
    DATA = yaml.load(f, Loader=yaml.loader.SafeLoader)

DATA_OUT = {}
for endpoint_path, endpoints_data in DATA.get("paths", {}).items():
    for verb in ["get", "post", "put", "delete"]:
        if endpoints_data.get(verb):
            operation_id = endpoints_data.get(verb, {})["operationId"]
            ref_req_in = endpoints_data.get(verb, {}).get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            ref_req_out = _check_refs( ref_req_in)
            ref_res_in = endpoints_data.get(verb, {}).get("responses", {}).get("200", {})
            ref_res_out = _check_refs(ref_res_in)
            if not DATA_OUT.get(endpoint_path):
                DATA_OUT[endpoint_path] = {}

            DATA_OUT[endpoint_path][operation_id] = {
                "request": ref_req_out,
                "response": ref_res_out
            }

with open(REF_FILE, "w") as f:
    yaml.dump(DATA_OUT, f)