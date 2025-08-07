"""
reordering the paths/responses/schemas/...
add missing response errors
"""

import yaml
import json

ORDER = ["openapi", "info", "servers", "security", "tags", "paths", "components"]

FILENAME = "openapi"
SRC_FILE = f"./{FILENAME}.yaml"


def display_mess(message):
    print("{0} ".format(message).ljust(79, "."), end="", flush=True)


def display_success():
    print("\033[92m\u2714\033[0m")


def display_failure():
    print("\033[31m\u2716\033[0m")

class NoAliasYamlDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def open_src():
    oas = ""
    display_mess("Opening file")
    try:
        with open(SRC_FILE, "r") as oas_in_file:
            oas = yaml.safe_load(oas_in_file)
        display_success()
        return oas
    except:
        display_failure()


def save_json(oas, filename):
    display_mess(f"Saving JSON to {filename}")
    try:
        with open(filename, "w") as oas_out_file:
            json.dump(oas, oas_out_file)
        display_success()
    except:
        display_failure()


def save_yaml(oas):
    display_mess(f"Saving YAML to {SRC_FILE}")
    try:
        with open(SRC_FILE, "w") as oas_out_file:
            for item in ORDER:
                yaml.dump({item: oas[item]}, oas_out_file, Dumper=NoAliasYamlDumper, default_flow_style=False)
        display_success()
    except:
        display_failure()


def sort_paths(oas):
    display_mess("Sort Paths")
    oas["paths"] = {k: oas["paths"][k] for k in sorted(oas["paths"])}
    try:
        display_success()
        return oas
    except:
        display_failure()


def sort_parameters(oas):
    display_mess("Sort Parameters")
    try:
        oas["components"]["parameters"] = {
            k: oas["components"]["parameters"][k]
            for k in sorted(oas["components"]["parameters"])
        }
        display_success()
        return oas
    except:
        display_failure()


def sort_responses(oas):
    display_mess("Sort Responses")
    try:
        oas["components"]["responses"] = {
            k: oas["components"]["responses"][k]
            for k in sorted(oas["components"]["responses"])
        }
        display_success()
        return oas
    except:
        display_failure()


def sort_schemas(oas):
    display_mess("Sort Schemas")
    try:
        oas["components"]["schemas"] = {
            k: oas["components"]["schemas"][k]
            for k in sorted(oas["components"]["schemas"])
        }
        display_success()
        return oas
    except:
        display_failure()





def add_response_vnd(oas):
    print(" application/vnd.api+json response header ".center(79, "-"))
    added = 0
    oas_responses = oas.get("components", {}).get("responses", {})
    #try:
    for response_name, response_data in oas_responses.items():
        if response_data.get("content", {}):
            if response_data.get("content", {}).get("application/json") and not response_data.get("content", {}).get("application/vnd.api+json"):
                display_mess(f"Adding application/vnd.api+json to {response_name}")
                oas["components"]["responses"][response_name]["content"]["application/vnd.api+json"] = {}
                response_examples = response_data["content"]["application/json"].get("examples")
                response_schema = response_data["content"]["application/json"].get("schema")
                if response_examples:
                    tmp = {}
                    for example_name, example_data in response_examples.items():
                        comp_example_name = f"{response_name}{example_name.replace(' ', '').replace('_', '').replace('-', '').replace('/', '')}"
                        oas["components"]["examples"][comp_example_name] = example_data
                        tmp[example_name] = {"$ref": f"#/components/examples/{comp_example_name}"}
                    if not oas["components"]["responses"][response_name]["content"]["application/vnd.api+json"].get("examples"):
                        oas["components"]["responses"][response_name]["content"]["application/vnd.api+json"]["examples"] = {}
                    oas["components"]["responses"][response_name]["content"]["application/json"]["examples"] = tmp
                    oas["components"]["responses"][response_name]["content"]["application/vnd.api+json"]["examples"] = tmp
                if response_schema:
                    if not oas["components"]["responses"][response_name]["content"]["application/vnd.api+json"].get("schema"):
                        oas["components"]["responses"][response_name]["content"]["application/vnd.api+json"]["schema"] = {}
                    oas["components"]["responses"][response_name]["content"]["application/json"]["schema"]= response_schema
                    oas["components"]["responses"][response_name]["content"]["application/vnd.api+json"]["schema"]= response_schema
                added += 1
                display_success()
            
    return oas
    
    # except Exception as e:
    #     display_failure()
    #     print(e)

if __name__ == "__main__":
    data = open_src()    
    data = add_response_vnd(data)
    save_yaml(data)
