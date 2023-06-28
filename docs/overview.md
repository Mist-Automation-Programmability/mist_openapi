---
stoplight-id: qhdjajymc505w
---

# Overview

## Object Models

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

## API Prefix

Current API version is v1. The intention is to maintain API version stability as much as possible.

API prefix : `/api/v1`

## HTTP Verbs

| Verb | Description |
| --- | --- |
| `GET` | Used for retrieving resources. |
| `POST` | Used for creating resources. |
| `PUT` | Used for replacing resources or collections. same payload as POST |
| `DELETE` | Used for deleting resources. |

## HTTP Response

We currently use few HTTP response codes:

| Status | Description |
| --- | --- |
| `200` | OK |
| `400` | Bad Request. The API endpoint exists but its syntax/payload is incorrect, detail may be given |
| `401` | Unauthorized |
| `403` | Permission Denied |
| `404` | Not found. The API endpoint doesn’t exist or resource doesn’t exist |

# CRUD

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

## Get a list of objects in a collection

```
GET /api/v1/sites/:site_id/:collection

```

### Response:

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

## Create an new object in a collection

```
POST /api/v1/sites/:site_id/collection

```

### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name` | `string` | name of the object |
| `color` | `string` | **Required**. red / green / blue |
| `object` | `object` | a nested object can be used. it will be shallow (at most 3 level, including list) |
| `list` | `list` | list of lucky numbers |

### Example

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

### Response

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

## Retrieve an object in a collection by id

```
GET /api/v1/sites/:site_id/:collection/:object_id

```

### Response

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

## Update an object in a colleciton

```
PUT /api/v1/sites/:site_id/wlans/:object_id
POST /api/v1/sites/:site_id/wlans/:object_id

```

### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name` | `string` | name of the object |
| `color` | `string` | **Required**. red / green / blue |
| `object` | `object` | a nested object can be used. it will be shallow (at most 3 level, including list) |
| `list` | `list` | list of lucky numbers |

### Response:

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

## Delete an object in a collection

```
DELETE /api/v1/sites/:site_id/:collection/:object_id

```

### Response

```
Status: 200 OK

```

# Permission

Mist API follow REST principles where GET requires `read` role, POST / PUT / DELETE requires `write` role.

## CSRF

All POST / PUT / DELETE APIs needs to have CSRF token in the AJAX Request header. This protects the website against [Cross Site Request Forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery).

```
X-CSRFToken: vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx

```

This token can be retrieved from the `cookies[csrftoken]`, which is sent during Login

# Query

## Pagination

Some of the queries supports pagination. Many of them are also time-based

```
?limit=100&page=1

```

### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `limit` | `int` | max number of results, default = 100 |
| `page` | `int` | page number (> 1), default is 1 |

### Response

```json
{
    "limit": 100,
    "page": 1,
    "total": 135,
    "results": [
        {
            // one log entry
        }
    ]
}

```

### Response Definitions

| Name | Type | Description |
| --- | --- | --- |
| `limit` | `int` | the limit |
| `page` | `int` | the page number |
| `total` | `int` | total number of results |
| `results` | `list` | list of results, len(results) <= limit |

## Pagination by HTTP Header

Many APIs provides an array as response for simplicity. When the amount of data is huge and pagination is desired, one can use HTTP Header in the GET request. And the `limit`, `page`, `total` will be returned in the HTTP Response Header as well.

### Request

| Name | Type | Description |
| --- | --- | --- |
| `X-Page-Limit` | `int` | the limit |
| `X-Page-Page` | `int` | the page number, default is 1 |

### Response

| Name | Type | Description |
| --- | --- | --- |
| `X-Page-Limit` | `int` | the limit |
| `X-Page-Page` | `int` | the page number |
| `X-Page-Total` | `int` | the total number of entries without pagination |

## Timestamp

Timestamps are always in UTC

## Time Range

For historical stats and/or logs where time range is needed, you can specify the time range in a few different ways:

| Query | Description |
| --- | --- |
| `?start=1430000000&end=1430864000` | specify the start / end |
| `?end=1430864000&duration=1d` | specify end time and duration |
| `?duration=1d` | specify duration, end will be now() in seconds |

## Aggregation

Aggregation works by giving a time range plus `interval` (e.g. `1d`, `1h`, `10m`) where aggregation function would be applied to.

Implementation-wise, aggregation happens at real time against fixed _windows_ or _bins_. E.g. for hourly aggregation, it will fall on 10:00-11:00 and not on 10:10-11:10.

That is, the query will be dynamically adjusted to align to the data available in our backend, with the actual start/end returned in the response. E.g. `?duration=1d&interval=1h` will give you latest 24 data points (end is implicitly now()). All time are in UTC.

# Websocket API

### Sample UI codes

```js


var conn = new WebSocket('wss://api-ws.mist.com/api-ws/v1/stream');
var max_msgs = 2;

conn.onopen = function(e){
    console.log('onopen', e);
    conn.send(JSON.stringify({"subscribe": "/test"}));
};

conn.onmessage = function(e){
    console.log('onmessage', e.data);
    if (max_msgs == 0) {
        conn.send(JSON.stringify({"unsubscribe": "/test"}));
    }
    else if (max_msgs < 0) {
        return;
    }
    max_msgs = max_msgs - 1;
};


Open JS Console!


```

expected output

```js
onopen > Event {isTrusted: true}
onmessage {"event": "channel_subscribed", "channel": "/test"}
onmessage {"data": "1", "event": "data", "channel": "/test"}
onmessage {"data": "1", "event": "data", "channel": "/test"}
onmessage {"event": "channel_unsubscribed", "channel": "/test"}

```

### Sample Python Code

```python
import base64
import json

import websocket  # websocket-client==0.44.0

msg_received = 0

email = 'your_email@here'
password = 'your_password'


def on_message(ws, message):
    global msg_received
    print('onmessage', message)
    msg_received += 1
    if msg_received > 3:
        ws.send(json.dumps({'unsubscribe': '/test'}))
        ws.close()


def on_error(ws, error):
    print('onerror')


def on_close(ws):
    print('onclose')


def on_open(ws):
    print('onopen')
    ws.send(json.dumps({'subscribe': '/test'}))


if __name__ == "__main__":
    header = ['Authorization: Basic %s' % (base64.b64encode(bytes(email + ':' + password, "UTF-8"))).decode('ascii')]
    ws = websocket.WebSocketApp("wss://api-ws.mist.com/api-ws/v1/stream",
                                header=header,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


```

# Rate Limit

The current rate limiting is 5000 API calls per hour and is reset at the hourly boundary. If you need more, please contact our support about your use case. It is possible that there are other APIs that can better serve you or new APIs we could have created to do what you’re trying to do.

NOTE: `/api/v1/login` is rate-limited much sooner (after 3 login failures) to prevent brute-force attack

### Response when the request is rate-limited

```
Status: 429 Too Many Requests
Retry-After: 798


```

# Mist Github Repo

Sample codes can be found on our [mist-public](https://github.com/mistsys/mist-public) Github.