Audit logs records all administrative activities done by current admin across all orgs

# Get a list of change logs across all Orgs for current admin

```
GET /api/v1/self/logs?start=1431384000&end=1431298000

```

### Response

```json
{
    "start": 1428939600,
    "end":   1428954000,
    "limit": 100,
    "page": 1,
    "total": 135,
    "results": [
        {
            "timestamp": 1431382121,
            "site_id": "4ac1dcf4-9d8b-7211-65c4-057819f0862b",
            "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71",
            "admin_id": "72bfa2bd-e58a-4670-9d20-a1468f7a6f58",
            "admin_name": "test@mistsys.com",
            "message": "Update WLAN \"Corporate\"",
            "id": "c6f9347b-b0a4-4a23-b927-fa9249f2ffb2",
            "before": {
                "auth": {
                    "type": "psk"
                }
            },
            "after": {
                "auth": {
                    "type": "open"
                }
            }
        }
    ]
}
```

### Response Definitions

see [Pagination](page:guides/overview/3_query#pagination)

| Name | Type | Description |
| --- | --- | --- |
| `timestamp` | `long` | start time, in epoch |
| `site_id` | `string` | site id |
| `org_id` | `string` | org id |
| `msp_id` | `string` | msp id |
| `admin_id` | `string` | admin id |
| `admin_name` | `string` | name of the admin that performs the action |
| `message` | `string` | log message |
| `before` | `object` | field values prior to the change |
| `after` | `object` | field values after the change |
