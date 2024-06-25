from dis import dis
import json
import yaml

POSTMAN_FILE = "../mist.postman.json"
POSTMAN_USAGE_FILE = "./mist.postman_usage.json"

OAS_FILE = "./mist.openapi.yml"
POSTMAN_ENV_FILE = "./../mist.postman_env.json"

def display_mess(message):
    print("{0} ".format(message).ljust(79, '.'), end="", flush=True)

def display_success():
    print("\033[92m\u2714\033[0m")

def display_failure():
    print('\033[31m\u2716\033[0m')

def add_usage():
    display_mess("Loading Postman collection")
    try:
        postman_json = {}
        with open(f"{POSTMAN_FILE}", 'r') as postman_data:
            postman_json = json.load(postman_data)
        display_success()
    except:
        display_failure()
        return

    display_mess("Loading Postman usage")
    try:
        postman_usage_json = {}
        with open(f"{POSTMAN_USAGE_FILE}", 'r') as postman_usage_data:
            postman_usage_json = json.load(postman_usage_data)
        display_success()
    except:
        display_failure()
        return

    items = postman_json["item"]
    items.insert(0, postman_usage_json)
    postman_json["item"] = items

    display_mess("Saving Postman collection with usage")
    try:
        with open(f"{POSTMAN_FILE}.new.json", 'w') as postman_data:
            json.dump(postman_json, postman_data)
        display_success()
    except:
        display_failure()
        return


def create_env():
    oas_json = {}

    display_mess("Loading OAS data")
    try:
        with open(OAS_FILE, 'r') as oas_data:
            oas_json = yaml.safe_load(oas_data)
        display_success()
    except:
        display_failure()
        return

    oas_params = oas_json["components"]["parameters"]
    post_params = [{"type": "string","value": "https://api.mist.com","key": "baseUrl"}]

    for key in oas_params:
        if oas_params[key]["in"] == "path":
            if not oas_params[key].get("schema"):
                print(f"{key} >> No Schema")
            elif not oas_params[key]["schema"].get("type"):
                print(f"{key} >> No Type")
            else:
                new_param = {
                    "key": oas_params[key]["name"],
                    "type": oas_params[key]["schema"]["type"],
                    "value": oas_params[key]["schema"].get("example", "")
                }
                post_params.append(new_param)

    display_mess("Saving Postman environment")
    try:
        with open(POSTMAN_ENV_FILE, "w") as f:
            json.dump(post_params, f)
        display_success()
    except:
        display_failure()
        return

if __name__ == "__main__":
    create_env()
    add_usage()
