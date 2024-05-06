# Self

Get ‘whoami’ and privileges (which org and which sites I have access to)

```
GET /api/v1/self

```

## Response if a valid session has been created

```json
Status: 200 OK

{
    "email": "test@mistsys.com",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "14081112222",
    "via_sso": false,
    "privileges": [
        {
            "scope": "org",
            "org_id": "9ff00eec-24f0-44d7-bda4-6238c81376ee",
            "name": "TestCompany",
            "role": "write",
            "views": ["location"],
            "msp_id": "9520c63a-f7b3-670c-0944-727774d5a722",
            "msp_name": "MSP",
            "msp_url": "https://...",
            "msp_logo_url": "https://.../logo/9520c63a-f7b3-670c-0944-727774d5a722.jpeg",
            "orggroup_ids": ["9ff00eec-24f0-44d7-bda4-6238c81376ee"],
        },
        {
            "scope": "site",
            "site_id": "d96e3952-53e8-4266-959a-45acd55f5114",
            "name": "Mist Office",
            "role": "admin",
            "org_id": "9ff00eec-24f0-44d7-bda4-6238c81376ee",
            "org_name": "TestCompany",
            "sitegroup_ids": ["581328b6-e382-f54e-c9dc-999983183a34"],
            "msp_id": "9520c63a-f7b3-670c-0944-727774d5a722",
            "msp_url": "https://...",
            "msp_logo_url": "https://.../logo/9520c63a-f7b3-670c-0944-727774d5a722.jpeg",
        },
        {
            "scope": "msp",
            "msp_id": "9520c63a-f7b3-670c-0944-727774d5a722",
            "name": "MSP",
            "msp_url": "https://...",
            "msp_logo_url": "https://.../logo/9520c63a-f7b3-670c-0944-727774d5a722.jpeg",
            "role": "admin"
        }
    ],
    "tags": [ "has_8021x", "mist" ]
}
```

## Definitions

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | email of logged-in user |
| `first_name` | `string` | first name of logged-in user |
| `last_name` | `string` | last name of logged-in user |
| `phone` | `string` | phone number (numbers only, including country code) |
| `via_sso` | `boolean` | if admin login is via sso (via_sso is more restricted, password and email cannot be changed) |
| `privileges` | `list` | list of permission-against-scope |

### Privilege Definition 

| Name | Type | Description |
| --- | --- | --- |
| `scope` | `string` | org / site / msp |
| `org_id` | `string` | id of the org |
| `org_name` | `string` | name of the org (for a site belonging to org) |
| `msp_id` | `string` | id of the MSP (if the org belongs to an MSP) |
| `msp_name` | `string` | name of the MSP (if the org belongs to an MSP) |
| `msp_url` | `string` | custom url of the MSP (if the MSP belongs to an Advanced tier) |
| `msp_logo_url` | `string` | logo of the MSP (if the MSP belongs to an Advanced tier) |
| `orggroup_ids` | `list` | list of orggroup ids (if the org belongs to an MSP) |
| `name` | `string` | name of the org/site/MSP depending on object scope |
| `role` | `string` | access permissions: admin / write / read / helpdesk / installer |
| `views` | `list` | list of UI views, see [supported UI views](https://api.mist.com/api/v1/docs/Org#Custom-Roles) |
| `site_id` | `string` | id of the site |
| `sitegroup_ids` | `list` | list of sitegroup ids |
| `tags` | `list` | list of strings indicating capabilities. e.g. what to show/hide/disable/enable for this user |
