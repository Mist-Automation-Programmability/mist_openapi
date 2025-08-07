import yaml

schemas = {}
with open("./openapi.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    PATHS = data.get("paths")

OPERATION_IDS = []
VERBS = ["get", "post", "put", "delete"]
ORDER = [
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components",
    "x-tagGroups",
]


CATEGORIES = {
    "MIST": {},
    "WLAN": {},
    "LAN": {},
    "WAN": {},
    "NAC": {},
    "LOCATION": {},
    "SAMPLES": {},
}

NEW = {}

TRIGGERS = {
    "MIST": [
        "/alarms",
        "/alarmtemplates",
        "/anomaly",
        "/app",
        "/call",
        "/cert",
        "/claim",
        "/clone",
        "/crl",
        "/inventory",
        "/jse",
        "/jsi",
        "/license",
        "/msp",
        "/pma",
        "/secpolic",
        "/setting",
        "/sitegroup",
        "/sitetemplate",
        "/sle",
        "/sso",
        "/ssoroles",
        "/subscription",
        "/synthetic_test",
        "/tickets",
        "/troubleshoot",
        "/uisetting",
        "/util",
        "/vars",
        "/webhooks",
        "/self",
        "/register",
        "/recover",
        "/logs",
        "/invite",
        "/admins",
        "/logout",
        "/login",
        "/installer",
        "/const"
    ],
    "WLAN": [
        "/wxtunnels",
        "/wxtags",
        "/wxrules",
        "/wlans",
        "/mxedge",
        "/rogue",
        "/rftemplate",
        "/rfdiag",
        "/mxtunnel",
        "/guest",
        "/aptemplate",
        "/template",
        "/tunnel",
        "/pskportal",
        "/mxtunnel",
        "/mxedge",
        "/mxcluster",
        "/mxedge",
        "/psk",
    ],
    "LAN": [
        "/wired_client",
        "/switch",
        "/port",
        "/discovered_switch",
        "/evpn_topolog",
        "/networktemplate",
    ],
    "WAN": [
        "/wan_client",
        "/vpn",
        "/gateway",
        "/bgp_peer",
        "/ssr",
        "/skyatp",
        "/service",
        "/servicepolic",
        "/otherdevice",
        "/network",
        "/gatewaytemplate",
        "/vpn_peer",
        "/ssr",
        "128trouter",
        "/idpprofile",
    ],
    "NAC": ["/nac_client", "/nactag", "/nacrule", "/mist_nac"],
    "LOCATION": [
        "{zone_type}",
        "/zone",
        "/vbeacon",
        "/sdkclient",
        "/map",
        "/filtered_asset",
        "/discovered_asset",
        "/beacon",
        "/asset",
        "/rssizone",
        "/location",
        "/assetfilter",
        "/sdktemplate",
        "/sdkinvite",
        "/mobile",
    ],
    "SAMPLES": ["/webhook_example"],
}

HARDCODED = {
    # ORG
    "/api/v1/orgs": ["MIST"],
    "/api/v1/orgs/{org_id}": ["MIST"],
    "/api/v1/orgs/{org_id}/stats": ["MIST"],
    "/api/v1/orgs/{org_id}/insights/sites-sle": ["MIST"],
    "/api/v1/orgs/{org_id}/insights/{metric}": ["MIST"],
    # ORG INVENTORY
    "/api/v1/orgs/{org_id}/inventory/create_ha_cluster": ["WAN"],
    # ORG TOKENS
    "/api/v1/orgs/{org_id}/apitokens": ["MIST"],
    "/api/v1/orgs/{org_id}/apitokens/{apitoken_id}": ["MIST"],
    # ORG SITES
    "/api/v1/orgs/{org_id}/sites": ["MIST"],
    "/api/v1/orgs/{org_id}/sites/count": ["MIST"],
    "/api/v1/orgs/{org_id}/sites/search": ["MIST"],
    # DEVICE PROFILES
    "/api/v1/orgs/{org_id}/deviceprofiles": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}/assign": ["WLAN","LAN","WAN",],
    "/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}/unassign": ["WLAN","LAN","WAN",],
    # DEVICE
    "/api/v1/orgs/{org_id}/devices": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/count": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/search": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/upgrade": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/upgrade/{upgrade_id}": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/events/count": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/events/search": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/last_config/count": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/last_config/search": ["WLAN", "LAN", "WAN"],
    "/api/v1/orgs/{org_id}/devices/radio_macs": ["WLAN"],
    "/api/v1/orgs/{org_id}/ocdevices/outbound_ssh_cmd": ["LAN", "WAN"],
    "/api/v1/orgs/{org_id}/stats/devices": ["WLAN", "LAN", "WAN"],
    # SITE
    "/api/v1/sites/{site_id}": ["MIST"],
    "/api/v1/sites/{site_id}/events/fast_roam": ["WLAN"],
    "/api/v1/sites/{site_id}/events/system/count": ["MIST"],
    "/api/v1/sites/{site_id}/events/system/search": ["MIST"],
    "/api/v1/sites/{site_id}/stats": ["MIST"],
    "/api/v1/sites/{site_id}/deviceprofiles/derived": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/rrm/current": ["WLAN"],
    "/api/v1/sites/{site_id}/rrm/events": ["WLAN"],
    "/api/v1/sites/{site_id}/rrm/optimize": ["WLAN"],
    "/api/v1/sites/{site_id}/rrm/current/devices/{device_id}/band/{band}": ["WLAN"],

    "/api/v1/sites/{site_id}/insights/{metric}": ["MIST"],
    # SITE DEVICE
    "/api/v1/sites/{site_id}/stats/devices": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/stats/devices/{device_id}": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/events/count": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/events/search": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/image{image_number}": ["WLAN","LAN","WAN",],
    "/api/v1/sites/{site_id}/devices/config_history/count": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/config_history/search": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/ap_channels": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/count": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/export": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/import": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/last_config/count": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/last_config/search": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/upgrade": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/upgrade_bios": ["LAN"],
    "/api/v1/sites/{site_id}/devices/upgrade/{upgrade_id}": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/upgrade/{upgrade_id}/cancel": ["WLAN","LAN","WAN",],
    "/api/v1/sites/{site_id}/devices/search": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/send_ble_beacon": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/reprovision": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/restart": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/versions": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/reset_radio_config": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/zeroize": ["LAN", "WAN"],
    "/api/v1/sites/{site_id}/insights/device/{device_mac}/{metric}": ["WLAN", "LAN", "WAN"],
    # DEVICE UTILS 
    "/api/v1/sites/{site_id}/devices/{device_id}/arp": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/bounce_port": ["LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/cable_test": ["LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/check_radius_server": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_arp": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_bgp": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_bpdu_error": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_macs": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/config_cmd": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/ha": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/iot": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/local_port_config": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/locate": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/unlocate": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/ping": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/poll_stats": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/readopt": ["LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/release_dhcp": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/request_ztp_password": ["LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/resolve_dns": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/restart": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_arp": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_mac_table": ["WLAN","LAN","WAN",],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_route": ["LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_service_path": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_session": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/snapshot": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/support": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/traceroute": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/upgrade": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/upgrade_bios": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/vc": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/vc/vc_port": ["LAN"],
    # ORG CLIENTS
    "/api/v1/orgs/{org_id}/clients/count": ["WLAN"],
    "/api/v1/orgs/{org_id}/clients/search": ["WLAN"],
    "/api/v1/orgs/{org_id}/clients/events/count": ["WLAN"],
    "/api/v1/orgs/{org_id}/clients/events/search": ["WLAN"],
    "/api/v1/orgs/{org_id}/clients/sessions/count": ["WLAN"],
    "/api/v1/orgs/{org_id}/clients/sessions/search": ["WLAN"],
    "/api/v1/orgs/{org_id}/clients/{client_mac}/coa": ["WLAN"],
    # SITE CLIENTS
    "/api/v1/sites/{site_id}/clients/count": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/disconnect": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/search": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/events/count": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/events/search": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/sessions/count": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/sessions/search": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/unauthorize": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/{client_mac}/coa": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/{client_mac}/disconnect": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/{client_mac}/events": ["WLAN"],
    "/api/v1/sites/{site_id}/clients/{client_mac}/unauthorize": ["WLAN"],
    "/api/v1/sites/{site_id}/insights/client/{client_mac}/{metric}": ["WLAN"],
    "/api/v1/sites/{site_id}/stats/clients": ["WLAN"],
    "/api/v1/sites/{site_id}/stats/clients/{client_mac}": ["WLAN"],
    "/api/v1/sites/{site_id}/stats/devices/{device_id}/clients": ["WLAN"],
    # PCAP
    "/api/v1/sites/{site_id}/pcaps": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/pcaps/capture": ["WLAN", "LAN", "WAN"],
    "/api/v1/sites/{site_id}/pcaps/{pcap_id}": ["WLAN", "LAN", "WAN"],

}


def menu(p):
    cats = []
    while True:
        print()
        i = 0
        for c in CATEGORIES:
            cats.append(c)
            print(f"{i}) {c}")
            i += 1
        o = input(f"{p} ?")
        try:
            res = cats[int(o)]
            return res
        except:
            print("wrong input")


def _set_tag(path, tags):
    properties = data["paths"][path]
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            operation_id = properties[verb]["operationId"]
            if not operation_id in OPERATION_IDS:
                OPERATION_IDS.append(operation_id)
            for t in tags:
                tag = f"tag1:{t}"
                if tag not in properties[verb]["tags"]:
                    # print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}: {tag}")
                    properties[verb]["tags"].append(tag)


for p in PATHS:
    done = False
    if p in HARDCODED:
        _set_tag(p, HARDCODED[p])
        done = True
    else:
        for c, trigger_list in TRIGGERS.items():
            for t in trigger_list:
                if t in p:
                    _set_tag(p, [c])
                    done = True
    if not done:
        _set_tag(p, [menu(p)])

with open("openapi_grp1.yaml", "w") as oas_out_file:
    for item in ORDER:
        yaml.dump({item: data[item]}, oas_out_file)

print(f"#OPERATIONS = {len(OPERATION_IDS)}")
