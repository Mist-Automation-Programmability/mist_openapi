# Object Models

```
+ MSP
|- + Organization
|--- + Site

```

- MSP: Optional, containing a group of orgs
- Organization: containing a group of sites, device, inventories, licenses, password policies, settings intended to be applied across sites
- Site: representing a project or a deployment, which contains a group of devices, a set of WLANs, policies, maps, zones, etc.
    

Take a shopping mall as an example, Westfield Group runs many shopping malls. Their IT buys APs, license. They manage inventories and may create a SSID, “Westfield-IT” for their purpose. Oakridge is one of their shopping malls, where they have local / smaller staff that runs day-to-day operations. There may be local SSID (e.g. Oakridge) and maps, zones associated. In the example, “Oakridge” is the Site. Westfield Group is the Org.

Org and Site are the two main API, with corresponding endpoints and privilege requirements.

# API Prefix

Current API version is v1. The intention is to maintain API version stability as much as possible.

API prefix : `/api/v1`

# HTTP Verbs

| Verb | Description |
| --- | --- |
| `GET` | Used for retrieving resources. |
| `POST` | Used for creating resources. |
| `PUT` | Used for replacing resources or collections. same payload as POST |
| `DELETE` | Used for deleting resources. |

# HTTP Response

We currently use few HTTP response codes:

| Status | Description |
| --- | --- |
| `200` | OK |
| `400` | Bad Request. The API endpoint exists but its syntax/payload is incorrect, detail may be given |
| `401` | Unauthorized |
| `403` | Permission Denied |
| `404` | Not found. The API endpoint doesn’t exist or resource doesn’t exist |
| `429` | Too Many Request. The API Token used for the request reached the 5000 API Calls per hour threshold |

