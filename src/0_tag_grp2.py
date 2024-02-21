import yaml


SPEC_FILE_IN="./tmp/mist.openapi_grp1.yml"
SPEC_FILE_OUT="./tmp/mist.openapi_grp2.yml"
LOGS = []

with open(SPEC_FILE_IN, "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


TAGS = [
    "CONSTANTS",
    "AUTHENTICATION",
    "MONITOR",
    "CONFIGURE"
]

verbs = ["get", "post", "put", "delete"]
order = [
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components",
    "x-tagGroups",
]



def ask_tag():
    while True:
        print("1) AUTHENTICATION")
        print("2) MONITOR")
        print("3) CONFIGURE")
        print("4) CONSTANTS")
        resp = input("tags? ")
        if resp == "1":
            return "AUTHENTICATION"
        if resp == "2":
            return "MONITOR"
        if resp == "3":
            return "CONFIGURE"
        if resp == "3":
            return "CONSTANTS"

def add_tag(new_tag, properties):
    for verb in properties:
        if verb in ["get", "post", "put", "delete"]:
            properties[verb]["tags"].append(f"tag2:{new_tag}")
            LOGS.append(f"{properties[verb]['operationId']} >>>> {new_tag}")


for path in data.get("paths", {}):
    properties = data["paths"][path]
    if "/api/v1/const/" in path:
        add_tag("CONSTANTS", properties)
    elif (
        path.startswith("/api/v1/login")
        or path.startswith("/api/v1/lookup")
        or path.startswith("/api/v1/tow_factor")
        or path.startswith("/api/v1/logout")
        or path.startswith("/api/v1/recover")
        or path.startswith("/api/v1/self")
    ):
        add_tag('AUTHENTICATION', properties)
        
    elif (
        "post" in properties
        or "delete" in properties
        or "put" in properties
        or ("get" in properties and (properties["get"]["operationId"].endswith("Derived") or properties["get"]["operationId"].startswith("test")))
        or  path.startswith("/api/v1/installer/")
    ):
        add_tag('CONFIGURE', properties)

    elif "get" in properties and (
        properties["get"]["operationId"].startswith("getSiteSle")
        or properties["get"]["operationId"].endswith("Events")
        or properties["get"]["operationId"].endswith("Logs")
        or properties["get"]["operationId"].endswith("Metrics")
        or properties["get"]["operationId"].startswith("count")
        or properties["get"]["operationId"].startswith("search")
        or "Stats" in properties["get"]["operationId"]
        ):
        add_tag('MONITOR', properties)

    else:
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                if properties[verb]["operationId"] in [
                    "listMspAdmins",
                    "getMspOrg",
                    "getMspSsoSamlMetadata",
                    "downloadMspSsoSamlMetadata",
                    "getOrg128TRegistrationCommands",
                    "listOrgAdmins",
                    "getOrgCertificates",
                    "getOrgCrlFile",
                    "listOrgDevices",
                    "getOrgMultiSitesUpgrade",
                    "listOrgGuestAuthorizations",
                    "listOrgJsiDevices",
                    "adoptOrgJsiDevice",
                    "getOrgMxEdgeUpgrade",
                    "getOrgMxEdgeUpgradeInfo",
                    "getOrgJuniperDevicesCommand",
                    "getSdkInviteQrCode",
                    "getOrgSsoSamlMetadata",
                    "downloadOrgSsoSamlMetadata",
                    "getOrgSsrUpgradeInfo",
                    "getOrgApplicationList",
                    "listSiteDevices",
                    "getSiteUpgrade",
                    "listSiteAvailableDeviceVersions",
                    "getSiteDeviceConfigCmd",
                    "listSiteRogueAPs",
                    "getSiteRogueAP",
                    "listSiteRogueClients",
                    "getSiteMachineLearningCurrentStat",
                    "getSiteDefaultPlfForModels",
                    "listSiteOtherDevices",
                    "listSitePacketCaptures",
                    "downloadSiteRfdiagRecording",
                    "getSiteSsrUpgrade",
                    "getSiteDerivedCurdSetting",
                    "getSiteApplicationList",
                    "listMspTickets",
                    "rebootOrgOtherDevice",
                    "listOrgAvailableSsrVersions",
                ]:
                    add_tag('CONFIGURE', properties)
                elif properties[verb]["operationId"] in [
                    "getMspSle",
                    "listMspOrgLicenses",
                    "getMspInventoryByMac",
                    "listMspLicenses",
                    "listMspSsoLatestFailures",
                    "listOrgApsMacs",
                    "getOrgSitesSle",
                    "getOrgSle",
                    "listOrgJsiPastPurchases",
                    "getOrgLicencesSummary",
                    "getOrgLicencesBySite",
                    "listOrgPmaDashboards",
                    "listOrgSsoLatestFailures",
                    "troubleshootOrgClient",
                    "getOrgCurrentMatchingClientsOfAWxTag",
                    "getSiteAnomalyEventsForClient",
                    "getSiteAnomalyEventsforDevice",
                    "listSiteApps",
                    "getSiteDeviceRadioChannels",
                    "exportSiteDevices",
                    "listSiteAllGuestAuthorizations",
                    "getSiteInsightMetricsForClient",
                    "getSiteInsightMetricsForDevice",
                    "getSiteInsightMetrics",
                    "getSiteLicenseUsage",
                    "getSiteBeamCoverageOverview",
                    "getSiteCurrentChannelPlanning",
                    "getSiteCurrentRrmConsiderationsForAnApOnASpecificBand",
                    "getSiteEventsForClient",
                    "listSiteDiscoveredAssets",
                    "getSiteDiscoveredSwitchesMetrics",
                    "getSiteAssetsOfInterest",
                    "getSiteDiscoveredAssetByMap",
                    "getSiteWxRulesUsage",
                    "getSiteCurrentMatchingClientsOfAWxTag",
                    "troubleshootOrg",
                    "getOrgJseInfo",
                    "getAdminRegistrationInfo",
                    "getSiteSpecificRrmConsiderations",
                    "getSiteJseInfo",
                    "troubleshootSiteCall"
                ]:
                    add_tag('MONITOR', properties)
                else:
                    new_tag = ask_tag()
                    add_tag(new_tag, properties)


with open(SPEC_FILE_OUT, "w") as oas_out_file:
    for item in order:
        yaml.dump({item: data[item]}, oas_out_file)

with open("./script.log", "w") as f:
    f.write("\n".join(LOGS))