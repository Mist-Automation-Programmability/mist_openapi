"""
This script is parsing the main openapi spec (single file) and add the type tag to each
endpoint based on the path
"""

import yaml


SPEC_FILE_IN = "../tmp/mist.openapi_grp1.yml"
SPEC_FILE_OUT = "../tmp/mist.openapi_grp2.yml"
LOGS = []

with open(SPEC_FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


TAGS = ["AUTHENTICATION", "MONITOR", "CONFIGURE", "UTILITIES"]

verbs = ["get", "post", "put", "delete"]
order = [
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components"
]

HARDCODED_PATH = {
    "/api/v1/sites/{site_id}/mxtunnels/{mxtunnel_id}/preempt_aps": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/send_ble_beacon": "UTILITIES",
    "/api/v1/sites/{site_id}/clients/{client_mac}/unauthorize": "UTILITIES",
    "/api/v1/sites/{site_id}/clients/{client_mac}/coa": "UTILITIES",
    "/api/v1/sites/{site_id}/clients/{client_mac}/disconnect": "UTILITIES",
    "/api/v1/sites/{site_id}/rogues/{rogue_bssid}/deauth_clients": "UTILITIES",
    "/api/v1/sites/{site_id}/clients/unauthorize": "UTILITIES",
    "/api/v1/sites/{site_id}/clients/disconnect": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/reprovision": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/reset_radio_config": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/zeroize": "UTILITIES",
    "/api/v1/sites/{site_id}/rrm/optimize": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_arp": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_bgp": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_bpdu_error": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/clear_macs": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/arp": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/bounce_port": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/cable_test": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/check_radius_server": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/poll_stats": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/readopt": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/release_dhcp": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/request_ztp_password": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/resolve_dns": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/restart": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/service_ping": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/show_arp": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/show_mac_table": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/show_route": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/show_service_path": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/show_session": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/snapshot": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/support": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/traceroute": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/locate": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/unlocate": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/upgrade": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/upgrade_bios": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/config_cmd": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/ping": "UTILITIES",
    "/api/v1/orgs/{org_id}/pcaps": "UTILITIES",
    "/api/v1/orgs/{org_id}/pcaps/capture": "UTILITIES",
    "/api/v1/orgs/{org_id}/pcaps/{pcap_id}": "UTILITIES",
    "/api/v1/sites/{site_id}/pcaps": "UTILITIES",
    "/api/v1/sites/{site_id}/pcaps/capture": "UTILITIES",
    "/api/v1/sites/{site_id}/pcaps/{pcap_id}": "UTILITIES",
    "/api/v1/sites/{site_id}/synthetic_test": "UTILITIES",
    "/api/v1/sites/{site_id}/devices/{device_id}/synthetic_test": "UTILITIES",
}
HARDCODED_OPERATION = {
    "listMspAdmins": "CONFIGURE",
    "getMspOrg": "CONFIGURE",
    "getMspSsoSamlMetadata": "CONFIGURE",
    "downloadMspSsoSamlMetadata": "CONFIGURE",
    "getOrg128TRegistrationCommands": "CONFIGURE",
    "listOrgAdmins": "CONFIGURE",
    "getOrgCertificates": "CONFIGURE",
    "getOrgCrlFile": "CONFIGURE",
    "listOrgDevices": "CONFIGURE",
    "getOrgMultiSitesUpgrade": "CONFIGURE",
    "listOrgGuestAuthorizations": "CONFIGURE",
    "listOrgJsiDevices": "CONFIGURE",
    "adoptOrgJsiDevice": "CONFIGURE",
    "getOrgMxEdgeUpgrade": "CONFIGURE",
    "getOrgMxEdgeUpgradeInfo": "CONFIGURE",
    "getOrgJuniperDevicesCommand": "CONFIGURE",
    "getSdkInviteQrCode": "CONFIGURE",
    "getOrgSsoSamlMetadata": "CONFIGURE",
    "downloadOrgSsoSamlMetadata": "CONFIGURE",
    "getOrgNacPortalSsoSamlMetadata": "CONFIGURE",
    "downloadOrgNacPortalSsoSamlMetadata": "CONFIGURE",
    "getOrgSsrUpgradeInfo": "CONFIGURE",
    "getOrgApplicationList": "CONFIGURE",
    "listSiteDevices": "CONFIGURE",
    "getSiteUpgrade": "CONFIGURE",
    "listSiteAvailableDeviceVersions": "CONFIGURE",
    "getSiteDeviceConfigCmd": "CONFIGURE",
    "listSiteRogueAPs": "CONFIGURE",
    "getSiteRogueAP": "CONFIGURE",
    "listSiteRogueClients": "CONFIGURE",
    "getSiteMachineLearningCurrentStat": "CONFIGURE",
    "getSiteDefaultPlfForModels": "CONFIGURE",
    "listSiteOtherDevices": "CONFIGURE",
    "listSitePacketCaptures": "CONFIGURE",
    "downloadSiteRfdiagRecording": "CONFIGURE",
    "getSiteSsrUpgrade": "CONFIGURE",
    "getSiteDerivedCurdSetting": "CONFIGURE",
    "getSiteApplicationList": "CONFIGURE",
    "rebootOrgOtherDevice": "CONFIGURE",
    "listOrgAvailableSsrVersions": "CONFIGURE",
    "getMspSle": "MONITOR",
    "listMspOrgLicenses": "MONITOR",
    "getMspInventoryByMac": "MONITOR",
    "listMspLicenses": "MONITOR",
    "listMspSsoLatestFailures": "MONITOR",
    "listOrgNacPortalSsoLatestFailures": "MONITOR",
    "listOrgApsMacs": "MONITOR",
    "getOrgSitesSle": "MONITOR",
    "getOrgSle": "MONITOR",
    "listOrgJsiPastPurchases": "MONITOR",
    "getOrgLicencesSummary": "MONITOR",
    "getOrgLicencesBySite": "MONITOR",
    "listOrgPmaDashboards": "MONITOR",
    "listOrgSsoLatestFailures": "MONITOR",
    "troubleshootOrgClient": "MONITOR",
    "getOrgCurrentMatchingClientsOfAWxTag": "MONITOR",
    "getSiteAnomalyEventsForClient": "MONITOR",
    "getSiteAnomalyEventsforDevice": "MONITOR",
    "listSiteApps": "MONITOR",
    "getSiteDeviceRadioChannels": "MONITOR",
    "exportSiteDevices": "MONITOR",
    "listSiteAllGuestAuthorizations": "MONITOR",
    "getSiteInsightMetricsForClient": "MONITOR",
    "getSiteInsightMetricsForDevice": "MONITOR",
    "getSiteInsightMetrics": "MONITOR",
    "getSiteLicenseUsage": "MONITOR",
    "getSiteBeamCoverageOverview": "MONITOR",
    "getSiteCurrentChannelPlanning": "MONITOR",
    "getSiteCurrentRrmConsiderations": "MONITOR",
    "getSiteCurrentRrmNeighbors": "MONITOR",
    "getSiteEventsForClient": "MONITOR",
    "listSiteDiscoveredAssets": "MONITOR",
    "getSiteDiscoveredSwitchesMetrics": "MONITOR",
    "getSiteAssetsOfInterest": "MONITOR",
    "getSiteDiscoveredAssetByMap": "MONITOR",
    "getSiteWxRulesUsage": "MONITOR",
    "getSiteCurrentMatchingClientsOfAWxTag": "MONITOR",
    "troubleshootOrg": "MONITOR",
    "getOrgJseInfo": "MONITOR",
    "getAdminRegistrationInfo": "MONITOR",
    "getSiteSpecificRrmConsiderations": "MONITOR",
    "getSiteJseInfo": "MONITOR",
    "troubleshootSiteCall": "MONITOR",
    "listSiteTroubleshootCalls": "MONITOR",
    "listMspTickets": "MONITOR",
}


def ask_tag(operationId):
    while True:
        print("1) AUTHENTICATION")
        print("2) MONITOR")
        print("3) CONFIGURE")
        print("4) UTILITIES")
        resp = input(f"tag for {operationId}? ")
        if resp == "1":
            return "AUTHENTICATION"
        if resp == "2":
            return "MONITOR"
        if resp == "3":
            return "CONFIGURE"
        if resp == "3":
            return "UTILITIES"


def add_tag(new_tag, properties):
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            properties[verb]["tags"].append(f"tag2:{new_tag}")
            LOGS.append(f"{properties[verb]['operationId']} >>>> {new_tag}")


for path in data.get("paths", {}):
    properties = data["paths"][path]
    if path in HARDCODED_PATH:
        add_tag(HARDCODED_PATH[path], properties)
    elif "/api/v1/const/" in path or "/webhook_example/" in path:
        pass
    elif (
        path.startswith("/api/v1/login")
        or path.startswith("/api/v1/lookup")
        or path.startswith("/api/v1/tow_factor")
        or path.startswith("/api/v1/logout")
        or path.startswith("/api/v1/recover")
        or path.startswith("/api/v1/self")
    ):
        add_tag("AUTHENTICATION", properties)

    elif (
        "post" in properties
        or "delete" in properties
        or "put" in properties
        or (
            "get" in properties
            and properties["get"]["operationId"].endswith("Derived")
        )
        or path.startswith("/api/v1/installer/")
    ):
        add_tag("CONFIGURE", properties)

    elif "get" in properties and (
        properties["get"]["operationId"].startswith("getSiteSle")
        or properties["get"]["operationId"].endswith("Events")
        or properties["get"]["operationId"].endswith("Logs")
        or properties["get"]["operationId"].endswith("Metrics")
        or properties["get"]["operationId"].startswith("count")
        or properties["get"]["operationId"].startswith("search")
        or "Stats" in properties["get"]["operationId"]
    ):
        add_tag("MONITOR", properties)

    else:
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                if properties[verb]["operationId"] in HARDCODED_OPERATION:
                    add_tag(
                        HARDCODED_OPERATION[properties[verb]["operationId"]],
                        properties
                    )
                else:                    
                    new_tag = ask_tag(properties[verb]["operationId"])
                    add_tag(new_tag, properties)


with open(SPEC_FILE_OUT, "w") as oas_out_file:
    for item in order:
        yaml.dump({item: data[item]}, oas_out_file)

with open("./script.log", "w") as f:
    f.write("\n".join(LOGS))
