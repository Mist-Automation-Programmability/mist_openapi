"""
This script is generating the toc files from the main openapi spec (single file) based on the documentation tag
Can be filtered to one or multiple spec files based on the .filters file
"""
import json
import re
import os
import sys
import yaml
import shutil

SPEC_FILE_IN = "./mist.openapi.yml"
SPEC_FILE_OUT = "./mistmcp.openapi.yml"
SPEC_FILE_OUT2 = "./mistmcp.openapi.json"
ROOT_ITEMS = [
    "self",
 #   "admins",
    "sites",
    "orgs",
 #   "msps",
 #   "installer",
 #   "utilities",
    "constants",
 #   "samples",
]

EXCLUDED_TAGS = [
    "Orgs Admins",
    "Orgs Alarm Templates",
    "Orgs AP Templates",
    "Orgs API Tokens",
    "Orgs Antivirus Profiles",
    "Orgs Asset Filters",
    "Orgs Assets",
    "Orgs Cert",
    "Orgs CRL",
    "Orgs Device Profiles",
    "Orgs EVPN Topologies",
    "Orgs Guests",
    "Orgs IDP Profiles",
    "Orgs JSI",
    "Orgs MxClusters",
    "Orgs MxEdges",
    "Orgs MxTunnels",
    "Orgs NAC Portals",
    "Orgs Devices - Others",
    "Orgs Premium Analytics",
    "Orgs Psks",
    "Orgs Psk Portals",
    "Orgs SDK Invites",
    "Orgs SDK Templates",
    "Orgs SecIntel Profiles",
    "Orgs Security Policies",
    "Orgs Integration JSE",
    "Orgs NAC CRL",
    "Orgs SCEP",
    "Orgs Integration SkyATP",
    "Orgs Integration Zscaler",
    "Orgs Linked Applications",
    "Orgs Site Templates",
    "Orgs SSO Roles",
    "Orgs SSO",
    "Orgs Stats - Assets",
    "Orgs Stats - MxEdges",
    "Orgs Stats - Other Devices",
    "Orgs Stats - Tunnels",
    "Orgs Tickets",
    "Orgs Webhooks",
    "Orgs WxRules",
    "Orgs WxTags",
    "Orgs WxTunnels",
    "Self API Token",
    "Self Alarms",
    "Self OAuth2",
    "Self MFA",
    "Sites AP Templates",
    "Sites Asset Filters",
    "Sites Assets",
    "Sites Beacons",
    "Sites Device Profiles",
    "Sites Devices - Wired - Virtual Chassis",
    "Sites EVPN Topologies",
    "Sites Gateway Templates",
    "Sites Guests",
    "Sites Licenses",
    "Sites Network Templates",
    "Sites Maps - Auto-placement",
    "Sites Maps - Auto-Zone",
    "Sites MxEdges",
    "Sites Devices - Others",
    "Sites SecIntel Profiles",
    "Sites JSE",
    "Sites Psks",
    "Sites RSSI Zones",
    "Sites Service Policies",
    "Sites Services",
    "Sites Site Templates",
    "Sites Skyatp",
    "Sites Stats - Assets",
    "Sites Stats - Beacons",
    "Sites Stats - Calls",
    "Sites Stats - Clients SDK",
    "Sites Stats - Discovered Switches",
    "Sites Stats - MxEdges",
    "Sites Stats - Zones",
    "Sites Stats - WxRules",
    "Sites UI Settings",
    "Sites VPNs",
    "Sites vBeacons",
    "Sites Webhooks",
    "Sites WxRules",
    "Sites WxTags",
    "Sites WxTunnels"
    "Sites Zones"
]

with open(SPEC_FILE_IN, "r") as f:
    DATA = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = DATA.get("paths")
    TAGS = DATA.get("tags")

PATHS_OUT={}
TAGS_OUT=[]
TAGS_LIST = []
for PATH, PATH_DATA in PATHS.items():
    path_out = {}
    if PATH_DATA.get("get") and not PATH_DATA["get"]["tags"][0] in EXCLUDED_TAGS:
        if PATH_DATA["get"]["tags"][0].split(" ")[0].lower() in ROOT_ITEMS:
            path_out["get"] = PATH_DATA["get"]
            if not PATH_DATA["get"]["tags"][0] in TAGS_LIST:
                TAGS_LIST.append(PATH_DATA["get"]["tags"][0])
    if path_out:
        PATHS_OUT[PATH] = path_out
        if PATH_DATA.get("parameters"):
            PATHS_OUT[PATH]["parameters"]= PATH_DATA.get("parameters")

for TAG in TAGS_LIST:
    tmp = next(item for item in TAGS if item["name"] == TAG)
    TAGS_OUT.append(tmp)

DATA["paths"] = PATHS_OUT
DATA["tags"] = TAGS_OUT

tmp = yaml.dump(DATA)
removed = 0
RESPONSE_OUT = {}
for RESPONSE, RESPONSE_DATA in DATA["components"]["responses"].items():
    if f"'#/components/responses/{RESPONSE}'" in tmp:
        RESPONSE_OUT[RESPONSE] = RESPONSE_DATA
    else:
        removed += 1
print(f"RESPONSE - removed: {removed}")

DATA["components"]["responses"] = RESPONSE_OUT

removed = 9
while removed > 0:
    removed = 0
    SCHEMAS_OUT = {}
    tmp = yaml.dump(DATA)
    for SCHEMA, SCHEMA_DATA in DATA["components"]["schemas"].items():
        if f"'#/components/schemas/{SCHEMA}'" in tmp:
            SCHEMAS_OUT[SCHEMA] = SCHEMA_DATA
        else:
            removed += 1
    print(f"SCHEMA - removed: {removed}")
    DATA["components"]["schemas"] = SCHEMAS_OUT


removed = 0
tmp = yaml.dump(DATA)
PARAMETER_OUT = {}
for PARAMETER, PARAMETER_DATA in DATA["components"]["parameters"].items():
    if f"'#/components/parameters/{PARAMETER}'" in tmp:
        PARAMETER_OUT[PARAMETER] = PARAMETER_DATA
    else:
        removed += 1
print(f"PARAMETER - removed: {removed}")

DATA["components"]["parameters"] = PARAMETER_OUT

with open(SPEC_FILE_OUT, "w") as f:
    yaml.dump({"openapi": DATA["openapi"]}, f)
    yaml.dump({"info": DATA["info"]}, f)
    yaml.dump({"servers": DATA["servers"]}, f)
    yaml.dump({"security": DATA["security"]}, f)
    yaml.dump({"tags": DATA["tags"]}, f)
    yaml.dump({"paths": DATA["paths"]}, f)
    yaml.dump({"components": DATA["components"]}, f)

with open(SPEC_FILE_OUT2, "w") as f:
    json.dump(DATA, f, indent=4, sort_keys=True, default=str)