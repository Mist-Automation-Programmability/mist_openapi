import yaml
import re
import json

schemas = {}
paths = {}

with open("mist.openapi.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


verbs = ["get", "post", "put", "delete"]
order = ["openapi", "info", "servers", "security", "tags", "paths", "components"]

manual_operation_ids = {
    "configuration": [
        "/api/v1/msps/{msp_id}/admins",
        "/api/v1/msps/{msp_id}/orgs/{org_id}",
        "/api/v1/msps/{msp_id}/ssos/{sso_id}/metadata",
        "/api/v1/msps/{msp_id}/ssos/{sso_id}/metadata.xml",
        "/api/v1/msps/{msp_id}/tickets",
        "/api/v1/orgs/{org_id}/128routers/register_cmd",
        "/api/v1/orgs/{org_id}/admins",
        "/api/v1/orgs/{org_id}/cert",
        "/api/v1/orgs/{org_id}/crl",
        "/api/v1/orgs/{org_id}/devices",
        "/api/v1/orgs/{org_id}/devices/upgrade/{upgrade_id}",
        "/api/v1/orgs/{org_id}/guests",
        "/api/v1/orgs/{org_id}/jsi/devices",
        "/api/v1/orgs/{org_id}/jsi/devices/outbound_ssh_cmd",
        "/api/v1/orgs/{org_id}/mxedges/upgrade/{upgrade_id}",
        "/api/v1/orgs/{org_id}/mxedges/version",
        "/api/v1/orgs/{org_id}/ocdevices/outbound_ssh_cmd",
        "/api/v1/orgs/{org_id}/sdkinvites/{sdkinvite_id}/qrcode",
        "/api/v1/orgs/{org_id}/ssos/{sso_id}/metadata",
        "/api/v1/orgs/{org_id}/ssos/{sso_id}/metadata.xml",
        "/api/v1/orgs/{org_id}/wxtags/apps",
        "/api/v1/sites/{site_id}/devices",
        "/api/v1/sites/{site_id}/devices/upgrade/{upgrade_id}",
        "/api/v1/sites/{site_id}/devices/versions",
        "/api/v1/sites/{site_id}/devices/{device_id}/config_cmd",
        "/api/v1/sites/{site_id}/location/ml/current",
        "/api/v1/sites/{site_id}/location/ml/defaults",
        "/api/v1/sites/{site_id}/otherdevices",
        "/api/v1/sites/{site_id}/pcaps",
        "/api/v1/sites/{site_id}/rfdiags/{rfdiag_id}/download",
        "/api/v1/sites/{site_id}/ssr/upgrade/{upgrade_id}",
        "/api/v1/sites/{site_id}/uisettings/derived",
        "/api/v1/sites/{site_id}/wxtags/apps",
        "/api/v1/orgs/{org_id}/ssr/versions",
        "/api/v1/orgs/{org_id}/junos/register_cmd",
        "/api/v1/sites/{site_id}/maps/{map_id}/revert_auto_orient",
        "/api/v1/sites/{site_id}/maps/{map_id}/revert_autoplacement"
    ],
    "monitor": [
        "/api/v1/sites/{site_id}/insights/rogues",
        "/api/v1/sites/{site_id}/rogues/{rogue_bssid}",
        "/api/v1/sites/{site_id}/insights/rogues/clients",
        "/api/v1/msps/{msp_id}/insights/{metric}",
        "/api/v1/msps/{msp_id}/stats/licenses",
        "/api/v1/msps/{msp_id}/inventory/{device_mac}",
        "/api/v1/msps/{msp_id}/licenses",
        "/api/v1/msps/{msp_id}/ssos/{sso_id}/failures",
        "/api/v1/orgs/{org_id}/devices/radio_macs",
        "/api/v1/orgs/{org_id}/insights/sites-sle",
        "/api/v1/orgs/{org_id}/insights/{metric}",
        "/api/v1/orgs/{org_id}/jsi/inventory",
        "/api/v1/orgs/{org_id}/licenses",
        "/api/v1/orgs/{org_id}/licenses/usages",
        "/api/v1/orgs/{org_id}/pma/dashboards",
        "/api/v1/orgs/{org_id}/ssos/{sso_id}/failures",
        "/api/v1/orgs/{org_id}/troubleshoot",
        "/api/v1/orgs/{org_id}/wxtags/{wxtag_id}/clients",
        "/api/v1/sites/{site_id}/anomaly/client/{client_mac}/{metric}",
        "/api/v1/sites/{site_id}/anomaly/device/{device_mac}/{metric}",
        "/api/v1/sites/{site_id}/apps",
        "/api/v1/sites/{site_id}/devices/ap_channels",
        "/api/v1/sites/{site_id}/devices/export",
        "/api/v1/sites/{site_id}/guests",
        "/api/v1/sites/{site_id}/insights/client/{client_mac}/{metric}",
        "/api/v1/sites/{site_id}/insights/device/{device_mac}/{metric}",
        "/api/v1/sites/{site_id}/insights/{metric}",
        "/api/v1/sites/{site_id}/licenses/usages",
        "/api/v1/sites/{site_id}/location/coverage",
        "/api/v1/sites/{site_id}/rrm/current",
        "/api/v1/sites/{site_id}/rrm/current/devices/{device_id}/band/{band}",
        "/api/v1/sites/{site_id}/clients/{client_mac}/events",
        "/api/v1/sites/{site_id}/stats/discovered_assets",
        "/api/v1/sites/{site_id}/stats/discovered_switches/metrics",
        "/api/v1/sites/{site_id}/stats/filtered_assets",
        "/api/v1/sites/{site_id}/stats/maps/{map_id}/discovered_assets",
        "/api/v1/sites/{site_id}/stats/wxrules",
        "/api/v1/sites/{site_id}/wxtags/{wxtag_id}/clients",
    ],
}

parts = {
    "openapi": data.get("openapi"),
    "info": data.get("info"),
    "servers": data.get("servers"),
    "security": data.get("security"),
    "tags": data.get("tags"),
    "paths": data.get("paths"),
    "components": data.get("components"),
    "x-tagGroups": data.get("x-tagGroups"),
}

cat_paths = {
    "constants": {},
    "authentication": {},
    "monitor": {"msps": {}, "orgs": {}, "sites": {}},
    "configuration": {"msps": {}, "orgs": {}, "sites": {}},
    "installer": {},
    "self": {},
    "webhook": {},
}

cat_params = {
    "constants": [],
    "authentication": [],
    "monitor": {"msps": [], "orgs": [], "sites": []},
    "configuration": {"msps": [], "orgs": [], "sites": []},
    "installer": [],
    "self": [],
    "webhook": [],
}
cat_responses = {
    "constants": [],
    "authentication": [],
    "monitor": {"msps": [], "orgs": [], "sites": []},
    "configuration": {"msps": [], "orgs": [], "sites": []},
    "installer": [],
    "self": [],
    "webhook": [],
}

cat_schemas = {
    "constants": [],
    "authentication": [],
    "monitor": {"msps": [], "orgs": [], "sites": []},
    "configuration": {"msps": [], "orgs": [], "sites": []},
    "installer": [],
    "self": [],
    "webhook": [],
}

cat_tags = {
    "constants": [],
    "authentication": [],
    "monitor": {"msps": [], "orgs": [], "sites": []},
    "configuration": {"msps": [], "orgs": [], "sites": []},
    "installer": [],
    "self": [],
    "webhook": [],
}

endpoints_count = {"get": 0, "post": 0, "put": 0, "delete": 0}

missing = []
logs = []


def add_endpoint(
    category: str,
    path: str,
    parameters: dict,
    verb: str,
    endpoint: dict,
    scope: str = None,
):
    print(category, path, verb, scope)
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
                    if not ref in cat_param:
                        cat_param.append(ref)
            cat_path[path] = {"parameters": parameters}
        else:
            cat_path[path] = {}

    endpoint_str = str(endpoint)

    re_schema = "\$ref'*: '#/components/schemas/([0-9a-zA-Z_.-]+)'"
    for entry in re.findall(re_schema, endpoint_str):
        if not entry in cat_schema:
            cat_schema.append(entry)

    re_parameters = "\$ref'*: '#/components/parameters/([0-9a-zA-Z_.-]+)'"
    for entry in re.findall(re_parameters, endpoint_str):
        if not entry in cat_param:
            cat_param.append(entry)

    re_responses = "\$ref'*: '#/components/responses/([0-9a-zA-Z._-]+)'"
    for entry in re.findall(re_responses, endpoint_str):
        if not entry in cat_response:
            cat_response.append(entry)

    for tag in endpoint.get("tags", []):
        if not tag in cat_tag:
            cat_tag.append(tag)

    cat_path[path][verb] = endpoint


def select_scope(endpoint: dict):
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


def split_scope(category: str, path: str, properties: dict):
    scope = path.split("/")[3]
    if scope in ["msps", "orgs", "sites"]:
        do_it(path, properties, category, scope)
        # add_endpoint(category, path, parameters, verb, endpoint, path.split("/")[3])
    # elif scope == "self":
    #     add_endpoint(category, path, parameters, verb, endpoint, "admins")
    elif (
        path.startswith("/api/v1/invite")
        or path.startswith("/api/v1/mobile")
        or path.startswith("/api/v1/register")
    ):
        do_it(path, properties, category, "orgs")
    elif path.startswith("/api/v1/utils"):
        do_it(path, properties, category, "sites")

    else:
        for verb in properties:
            if verb in verbs:
                scope = select_scope(properties[verb])
                do_it_one(path, properties[verb], category, scope)
        # add_endpoint(category, path, parameters, verb, endpoint, scope)


def ask_tag():
    while True:
        print("1) Authentication")
        print("2) Monitor")
        print("3) Configuration")
        print("4) Installer")
        resp = input("tags? ")
        if resp == "1":
            return "authentication"
        if resp == "2":
            return "monitor"
        if resp == "3":
            return "configuration"
        if resp == "3":
            return "installer"


def do_it(path, properties, category, scope: str = None):
    for verb in properties:
        if verb in verbs:
            logs.append(f"{properties[verb]['operationId']} >>>> {category}")
            endpoints_count[verb] += 1
            add_endpoint(
                category,
                path,
                properties.get("parameters"),
                verb,
                properties[verb],
                scope,
            )


def do_it_one(path, properties, category, verb, scope: str = None):
    logs.append(f"{properties[verb]['operationId']} >>>> Monitor")
    endpoints_count[verb] += 1
    add_endpoint(
        category, path, properties.get("parameters"), verb, properties[verb], scope
    )


def split():
    for path in data.get("paths", {}):
        print(f"{path} ".ljust(80, "-"))
        properties = data["paths"][path]

        if path.startswith("/webhook_example"):
            do_it(path, properties, "webhook")

        elif path.startswith("/api/v1/self"):
            do_it(path, properties, "self")
        

        elif (
            path.startswith("/api/v1/login")
            or path.startswith("/api/v1/logout")
            or path.startswith("/api/v1/recover")
        ):
            do_it(path, properties, "authentication")

        elif path.startswith("/api/v1/const"):
            do_it(path, properties, "constants")

        elif path.startswith("/api/v1/installer/"):
            do_it(path, properties, "installer")

        elif (
            "post" in properties
            or "delete" in properties
            or "put" in properties
            or (
                "get" in properties
                and (
                    properties["get"]["operationId"].endswith("Derived")
                    or properties["get"]["operationId"].startswith("test")
                )
            )
        ):
            split_scope("configuration", path, properties)

        elif "get" in properties and (
            properties["get"]["operationId"].startswith("getSiteSle")
            or properties["get"]["operationId"].endswith("Events")
            or properties["get"]["operationId"].endswith("Logs")
            or properties["get"]["operationId"].endswith("Metrics")
        ):
            split_scope("monitor", path, properties)

        elif "get" in properties and (
            properties["get"]["operationId"].startswith("count")
            or properties["get"]["operationId"].startswith("search")
            or "Stats" in properties["get"]["operationId"]
        ):
            split_scope("monitor", path, properties)
        elif path in manual_operation_ids["configuration"]:
            split_scope("configuration", path, properties)
        elif path in manual_operation_ids["monitor"]:
            split_scope("monitor", path, properties)

        else:
            category = ask_tag()
            do_it(path, properties, category)


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
    # if dst_parameters: components["schemas"] = dst_schemas
    return dst_schemas


def save_file(
    filename: str,
    cat_path: dict,
    cat_schema: dict,
    cat_param: list,
    cat_response: list,
    cat_tag: list,
):
    components = {}
    additional_schemas = []

    src_parameters = parts.get("components", {}).get("parameters")
    dst_parameters = {}
    for param in src_parameters:
        if param in cat_param:
            dst_parameters[param] = src_parameters[param]
    if dst_parameters:
        components["parameters"] = dst_parameters

    src_responses = parts.get("components", {}).get("responses")
    dst_responses = {}
    for response_def in cat_response:
        dst_responses[response_def] = src_responses[response_def]
        response_str = str(src_responses[response_def])
        re_responses = "\$ref'*: '#/components/schemas/([a-zA-Z_.-]+)'"
        for entry in re.findall(re_responses, response_str):
            if not entry in additional_schemas:
                additional_schemas.append(entry)

    if dst_parameters:
        components["responses"] = dst_responses

    schemas = cat_schema + additional_schemas
    dst_schemas = get_schemas(parts.get("components", {}).get("schemas"), schemas)
    if dst_parameters:
        components["schemas"] = dst_schemas

    tags = []
    for tag in parts.get("tags"):
        if tag.get("name") in cat_tag:
            tags.append(tag)

    data = {
        "openapi": parts.get("openapi"),
        "info": parts.get("info"),
        "servers": parts.get("servers"),
        "tags": tags,
        "paths": cat_path,
        "components": {"parameters": dst_parameters, "responses": dst_responses},
    }
    if not "authentication" in filename and not "webhook"  in filename :
        data["security"] = parts.get("security")
        data["components"]["securitySchemes"] = parts.get("components", {}).get(
            "securitySchemes"
        )

    output_str = json.dumps(data)
    re_schema = '\$ref"*: "#/components/schemas/([0-9a-zA-Z_.-]+)"'
    for entry in re.findall(re_schema, output_str):
        tmp_re_schema = f'\$ref"*: "#/components/schemas/{entry}"'
        output_str = re.sub(
            tmp_re_schema, f'$ref": "./components/schemas/{entry}.yaml"', output_str
        )
    data = json.loads(output_str)

    with open(filename, "w") as oas_out_file:
        for item in order:
            if item in data:
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
                save_file(
                    filename, cat_path, cat_schema, cat_param, cat_response, cat_tag
                )
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
    print(
        f"TOTAL : {endpoints_count['get'] + endpoints_count['post'] +endpoints_count['put'] +endpoints_count['delete'] }"
    )
