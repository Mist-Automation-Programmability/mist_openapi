"""
reordering the paths/responses/schemas/...
add missing response errors
"""

import yaml
import json

ORDER = ["openapi", "info", "servers", "security", "tags", "paths", "components"]

FILENAME = "mist.openapi"
SRC_FILE = f"./{FILENAME}.yaml"


def display_mess(message):
    print("{0} ".format(message).ljust(79, "."), end="", flush=True)


def display_success():
    print("\033[92m\u2714\033[0m")


def display_failure():
    print("\033[31m\u2716\033[0m")


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
                yaml.dump({item: oas[item]}, oas_out_file)
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


def add_default_responses(oas):
    crud = ["get", "post", "put", "delete"]
    display_mess("Adding Missing Default Responses")
    added = {
        "400": 0,
        "401": 0,
        "403": 0,
        "404": 0,
        "429": 0,
    }
    try:
        paths = oas["paths"]
        for endpoint in paths:
            if endpoint.startswith("/api/") and endpoint != "/api/v1/login":
                for verb in crud:
                    if verb in paths[endpoint]:
                        if "400" not in paths[endpoint][verb]["responses"]:
                            paths[endpoint][verb]["responses"]["400"] = {
                                "$ref": "#/components/responses/HTTP400"
                            }
                            added["400"] += 1
                        if "401" not in paths[endpoint][verb]["responses"]:
                            paths[endpoint][verb]["responses"]["401"] = {
                                "$ref": "#/components/responses/HTTP401"
                            }
                            added["401"] += 1
                        if "403" not in paths[endpoint][verb]["responses"]:
                            paths[endpoint][verb]["responses"]["403"] = {
                                "$ref": "#/components/responses/HTTP403"
                            }
                            added["403"] += 1
                        if "404" not in paths[endpoint][verb]["responses"]:
                            paths[endpoint][verb]["responses"]["404"] = {
                                "$ref": "#/components/responses/HTTP404"
                            }
                            added["404"] += 1
                        if "429" not in paths[endpoint][verb]["responses"]:
                            paths[endpoint][verb]["responses"]["429"] = {
                                "$ref": "#/components/responses/HTTP429"
                            }
                            added["429"] += 1
        oas["paths"] = paths
        display_success()
        print(added)
        return oas
    except Exception as e:
        display_failure()
        print(e)

if __name__ == "__main__":
    data = open_src()
    data = add_default_responses(data)
    data = sort_paths(data)
    data = sort_parameters(data)
    data = sort_responses(data)
    data = sort_schemas(data)
    save_yaml(data)
