"""
This script is parsing the main openapi spec (single file) and add the category tag to each
endpoint based on the path
"""
import yaml

SPEC_FILE_IN="./mist.openapi.yml"
SPEC_FILE_OUT="./tmp/mist.openapi_grp1.yml"


with open(SPEC_FILE_IN, "r") as f:
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

TAGS = [
    "MIST",
    "WLAN",
    "LAN",
    "WAN",
    "NAC",
    "LOCATION",
    "SAMPLES",
]

NEW = {}

TRIGGERS = {
    "MIST": [
        "/alarms",
        "/alarmtemplates",
        "/anomaly",
        "{site_id}/apps",
        "/stats/apps",
        "/call",
        "/cert",
        "/claim",
        "{org_id}/clone",
        "/crl",
        "/inventory",
        "/jse",
        "/jsi",
        "/license",
        "/msp",
        "/pma",
        "/maps",
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
        "/api/v1/register",
        "/recover",
        "self/logs",
        "{msp_id}/logs",
        "{org_id}/logs",
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
        "/pskportals",
        "/mxtunnel",
        "/mxedge",
        "/mxcluster",
        "/mxedge",
        "/psk",
    ],
    "LAN": [
        "/wired_clients",
        "/switch",
        "/ports",
        "/discovered_switch",
        "/evpn_topologies",
        "/networktemplates",
    ],
    "WAN": [
        "/128routers",
        "/zscaler",
        "/wan_client",
        "/vpn",
        "/gateway",
        "/bgp_peer",
        "/ssr",
        "/skyatp",
        "{org_id}/services",
        "{org_id}/servicepolicies",
        "/otherdevice",
        "{org_id}/networks",
        "{org_id}/gatewaytemplates",
        "{site_id}/services",
        "{site_id}/networks",
        "{site_id}/servicepolicies",
        "/vpn_peer",
        "/ssr",
        "/idpprofile",
    ],
    "NAC": ["/nac_client", "/nactag", "/nacrule", "/mist_nac"],
    "LOCATION": [
        "{zone_type}",
        "/zone",
        "/vbeacon",
        "/sdkclient",
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
    "/api/v1/orgs/{org_id}/deviceprofiles": ["MIST"],
    "/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}": ["MIST"],
    "/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}/assign": ["MIST",],
    "/api/v1/orgs/{org_id}/deviceprofiles/{deviceprofile_id}/unassign": ["MIST",],
    # DEVICE
    "/api/v1/orgs/{org_id}/devices": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/count": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/search": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/upgrade": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/upgrade/{upgrade_id}": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/events/count": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/events/search": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/last_config/count": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/last_config/search": ["MIST"],
    "/api/v1/orgs/{org_id}/devices/radio_macs": ["WLAN"],
    "/api/v1/orgs/{org_id}/ocdevices/outbound_ssh_cmd": ["MIST"],
    "/api/v1/orgs/{org_id}/stats/devices": ["MIST"],
    "/api/v1/orgs/{org_id}/mxedges/claim": ["MIST"],
    # SITE
    "/api/v1/sites/{site_id}": ["MIST"],
    "/api/v1/sites/{site_id}/events/fast_roam": ["WLAN"],
    "/api/v1/sites/{site_id}/events/system/count": ["MIST"],
    "/api/v1/sites/{site_id}/events/system/search": ["MIST"],
    "/api/v1/sites/{site_id}/stats": ["MIST"],
    "/api/v1/sites/{site_id}/deviceprofiles/derived": ["MIST"],
    "/api/v1/sites/{site_id}/rrm/current": ["WLAN"],
    "/api/v1/sites/{site_id}/rrm/events": ["WLAN"],
    "/api/v1/sites/{site_id}/rrm/optimize": ["WLAN"],
    "/api/v1/sites/{site_id}/rrm/current/devices/{device_id}/band/{band}": ["WLAN"],

    "/api/v1/sites/{site_id}/insights/{metric}": ["MIST"],
    # SITE DEVICE
    "/api/v1/sites/{site_id}/stats/devices": ["MIST"],
    "/api/v1/sites/{site_id}/stats/devices/{device_id}": ["MIST"],
    "/api/v1/sites/{site_id}/devices": ["MIST"],
    "/api/v1/sites/{site_id}/devices/events/count": ["MIST"],
    "/api/v1/sites/{site_id}/devices/events/search": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/image{image_number}": ["MIST",],
    "/api/v1/sites/{site_id}/devices/config_history/count": ["MIST"],
    "/api/v1/sites/{site_id}/devices/config_history/search": ["MIST"],
    "/api/v1/sites/{site_id}/devices/ap_channels": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/count": ["MIST"],
    "/api/v1/sites/{site_id}/devices/export": ["MIST"],
    "/api/v1/sites/{site_id}/devices/import": ["MIST"],
    "/api/v1/sites/{site_id}/devices/last_config/count": ["MIST"],
    "/api/v1/sites/{site_id}/devices/last_config/search": ["MIST"],
    "/api/v1/sites/{site_id}/devices/upgrade": ["MIST"],
    "/api/v1/sites/{site_id}/devices/upgrade_bios": ["LAN"],
    "/api/v1/sites/{site_id}/devices/upgrade/{upgrade_id}": ["MIST"],
    "/api/v1/sites/{site_id}/devices/upgrade/{upgrade_id}/cancel": ["MIST",],
    "/api/v1/sites/{site_id}/devices/search": ["MIST"],
    "/api/v1/sites/{site_id}/devices/send_ble_beacon": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/restart": ["MIST"],
    "/api/v1/sites/{site_id}/devices/versions": ["MIST"],
    "/api/v1/sites/{site_id}/devices/reset_radio_config": ["WLAN"],
    "/api/v1/sites/{site_id}/devices/zeroize": ["WLAN"],    
    "/api/v1/sites/{site_id}/devices/reprovision": ["WLAN"],
    "/api/v1/sites/{site_id}/insights/device/{device_mac}/{metric}": ["MIST"],
    # DEVICE UTILS
    "/api/v1/sites/{site_id}/devices/{device_id}/arp": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/service_ping": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/bounce_port": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/cable_test": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/check_radius_server": ["LAN"],
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
    "/api/v1/sites/{site_id}/devices/{device_id}/ping": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/poll_stats": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/readopt": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/release_dhcp": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/request_ztp_password": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/resolve_dns": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/restart": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_arp": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_mac_table": ["MIST",],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_route": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_service_path": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/show_session": ["WAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/snapshot": ["LAN"],
    "/api/v1/sites/{site_id}/devices/{device_id}/support": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/traceroute": ["MIST"],
    "/api/v1/sites/{site_id}/devices/{device_id}/upgrade": ["MIST"],
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
    "/api/v1/sites/{site_id}/pcaps": ["MIST"],
    "/api/v1/sites/{site_id}/pcaps/capture": ["MIST"],
    "/api/v1/sites/{site_id}/pcaps/{pcap_id}": ["MIST"],
    # NAC
    "/api/v1/orgs/{org_id}/setting/mist_nac_crls": ["NAC"],
    "/api/v1/orgs/{org_id}/setting/mist_nac_crls/{naccrl_id}": ["NAC"],
    #ZSCALER
    "/api/v1/orgs/{org_id}/setting/zscaler/setup": ["WAN"],
    #LOCATION
    "/api/v1/sites/{site_id}/stats/maps/{map_id}/discovered_assets": ["LOCATION"],
    "/api/v1/sites/{site_id}/stats/maps/{map_id}/sdkclients": ["LOCATION"],
}


def menu(p):
    cats = []
    while True:
        print()
        i = 0
        for c in TAGS:
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
            if (
                path.startswith("/api/v1/const")
                or path.startswith("/api/v1/installer")
            ):
                tag = f"tag1:MIST"
                if tag not in properties[verb]["tags"]:
                    properties[verb]["tags"].append(tag)
            else:
                for t in tags:
                    tag = f"tag1:{t}"
                    if tag not in properties[verb]["tags"]:
                        properties[verb]["tags"].append(tag)
            # toc_tag = t
            # if toc_tag:
            #     properties[verb]["tags"].append(toc_tag)


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

with open(SPEC_FILE_OUT, "w") as oas_out_file:
    for item in ORDER:
        yaml.dump({item: data[item]}, oas_out_file)

print(f"#OPERATIONS = {len(OPERATION_IDS)}")
