CRUD operation against resources/collections are RESTful with URIs like

| URI | Description |
| --- | --- |
| `/api/v1/orgs/:org_id` | org |
| `/api/v1/orgs/:org_id/sites` | all sites under a org |
| `/api/v1/sites/:site_id` | site |
| `/api/v1/sites/:site_id/wlans` | all wlans under a site |
| `/api/v1/sites/:site_id/wlans/:wlan_id` | wlan |

As site is equivalent to a project from MSP’s perspective (e.g. a mall, a hospital, a school), we’ll use it as context when we describe generic RESTful operations.

Site collections are accessible through RESTful site-resource URIs.

```
/api/v1/sites/:site_id/:collection

```

Only users with _admin_ role (see [Auth](https://api.mist.com/api/v1/docs/Auth#self)) against the target :site_id can perform POST/PUT/DELETE. GET operation requires _readonly_ role.

# Get a list of objects in a collection

```
GET /api/v1/sites/:site_id/:collection

```

#### Response:

```json
Status: 200 OK

[
    {
        "id": "445c23ed-f8ec-cf05-24ea-64af335cb575",
        "name": "object name",
        "attr": "value",
        "object": {
            "nested": true
        },
        "list": [ "value1", "value2" ]
    }
    , ...
]

```

# Create an new object in a collection

```
POST /api/v1/sites/:site_id/collection

```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name` | `string` | name of the object |
| `color` | `string` | **Required**. red / green / blue |
| `object` | `object` | a nested object can be used. it will be shallow (at most 3 level, including list) |
| `list` | `list` | list of lucky numbers |

#### Example

```json
Status: 200 OK

{
    "name": "object name",
    "attr": "value",
    "object": {
        "nested": true
    },
    "list": [ "value1", "value2" ]
}

```

#### Response

```json
Status: 200 OK

{
    "id": "445c23ed-f8ec-cf05-24ea-64af335cb575",
    "name": "object name",
    "attr": "value",
    "object": {
        "nested": true
    },
    "list": [ "value1", "value2" ]
}

```

# Retrieve an object in a collection by id

```
GET /api/v1/sites/:site_id/:collection/:object_id

```

#### Response

```json
Status: 200 OK

{
    "id": "445c23ed-f8ec-cf05-24ea-64af335cb575",
    "name": "object name",
    "attr": "value",
    "object": {
        "nested": true
    },
    "list": [ "value1", "value2" ]
}

```

# Update an object in a colleciton

```
PUT /api/v1/sites/:site_id/wlans/:object_id
POST /api/v1/sites/:site_id/wlans/:object_id

```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name` | `string` | name of the object |
| `color` | `string` | **Required**. red / green / blue |
| `object` | `object` | a nested object can be used. it will be shallow (at most 3 level, including list) |
| `list` | `list` | list of lucky numbers |

#### Response:

```json
Status: 200 OK

{
    "id": "445c23ed-f8ec-cf05-24ea-64af335cb575",
    "name": "object name",
    "attr": "value",
    "object": {
        "nested": true
    },
    "list": [ "value1", "value2" ]
}

```

# Delete an object in a collection

```
DELETE /api/v1/sites/:site_id/:collection/:object_id

```

#### Response

```
Status: 200 OK

```