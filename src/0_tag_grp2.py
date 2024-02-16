import yaml

schemas = {}
paths = {}
with open("mist.openapi_grp1.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)


cat = ["Constants", "Authentication", "Monitor", "Configure"]
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


for i in schemas:
    data = schemas[i]
    model = {
        "title": i,
        "type": data.get("type"),
    }
    if data.get("items"):
        model["items"] = data.get("items")
    if data.get("properties"):
        model["properties"] = data.get("properties")
    if data.get("description"):
        model["description"] = data.get("description")
    if data.get("required"):
        model["required"] = data.get("required")

logs = []


def ask_tag():
    while True:
        #print("1) Authentication")
        #print("2) Monitor")
        #print("3) Configure")
        #print("4) Installer")
        resp = input("tags? ")
        if resp == "1":
            return "Authentication"
        if resp == "2":
            return "Monitor"
        if resp == "3":
            return "Configure"
        if resp == "3":
            return "Installer"


for path in data.get("paths", {}):
    #print(path)
    properties = data["paths"][path]
    if path.startswith("/api/v1/installer/"):
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                #print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                properties[verb]["tags"].append("cat2:INSTALLER")
                logs.append(f"{properties[verb]['operationId']} >>>> Installer")
    elif (
        path.startswith("/api/v1/login")
        or path.startswith("/api/v1/lookup")
        or path.startswith("/api/v1/tow_factor")
        or path.startswith("/api/v1/logout")
        or path.startswith("/api/v1/recover")
    ):
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                #print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                properties[verb]["tags"].append("cat2:AUTHENTICATION")
                logs.append(f"{properties[verb]['operationId']} >>>> Authentication")
    elif path.startswith("/api/v1/self"):
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                #print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                properties[verb]["tags"].append("cat2:SELF")
                logs.append(f"{properties[verb]['operationId']} >>>> Self")
    elif (
        "post" in properties
        or "delete" in properties
        or "put" in properties
        or ("get" in properties and (properties["get"]["operationId"].endswith("Derived") or properties["get"]["operationId"].startswith("test")))
    ):
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                #print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                properties[verb]["tags"].append("cat2:CONFIGURE")
                logs.append(f"{properties[verb]['operationId']} >>>> Configure")

    elif "get" in properties and (
        properties["get"]["operationId"].startswith("getSiteSle")
        or properties["get"]["operationId"].endswith("Events")
        or properties["get"]["operationId"].endswith("Logs")
        or properties["get"]["operationId"].endswith("Metrics")
        ):
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                #print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                properties[verb]["tags"].append("cat2:MONITOR")
                logs.append(f"{properties[verb]['operationId']} >>>> Monitor")

    else:
        for verb in properties:
            if verb in ["get", "post", "put", "delete"]:
                #print(f">>>>>>>>>>>>>>>>> {properties[verb]['operationId']}")
                if not "Constants" in properties[verb]["tags"]:
                    if (
                        properties[verb]["operationId"].startswith("count")
                        or properties[verb]["operationId"].startswith("search")
                        or "Stats" in properties[verb]["operationId"]
                    ):
                        logs.append(f"{properties[verb]['operationId']} >>>> Monitor")
                        properties[verb]["tags"].append("cat2:MONITOR")
                    else:
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
                            properties[verb]["tags"].append("cat2:CONFIGURE")
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
                            properties[verb]["tags"].append("cat2:MONITOR")
                        else:
                            new_tag = ask_tag()
                            if not new_tag in properties[verb]["tags"]:
                                logs.append(
                                    f"{properties[verb]['operationId']} >>>> {new_tag}"
                                )
                                properties[verb]["tags"].append(new_tag)


with open("mist.openapi_grp2.yml", "w") as oas_out_file:
    for item in order:
        yaml.dump({item: data[item]}, oas_out_file)

with open("./script.log", "w") as f:
    f.write("\n".join(logs))