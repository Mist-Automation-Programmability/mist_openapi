# Pagination

Some of the queries supports pagination. Many of them are also time-based

```
?limit=100&page=1

```

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `limit` | `int` | max number of results, default = 100 |
| `page` | `int` | page number (> 1), default is 1 |

#### Response

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

#### Response Definitions

| Name | Type | Description |
| --- | --- | --- |
| `limit` | `int` | the limit |
| `page` | `int` | the page number |
| `total` | `int` | total number of results |
| `results` | `list` | list of results, len(results) <= limit |

# Pagination by HTTP Header

Many APIs provides an array as response for simplicity. When the amount of data is huge and pagination is desired, one can use HTTP Header in the GET request. And the `limit`, `page`, `total` will be returned in the HTTP Response Header as well.

#### Request

| Name | Type | Description |
| --- | --- | --- |
| `X-Page-Limit` | `int` | the limit |
| `X-Page-Page` | `int` | the page number, default is 1 |

#### Response

| Name | Type | Description |
| --- | --- | --- |
| `X-Page-Limit` | `int` | the limit |
| `X-Page-Page` | `int` | the page number |
| `X-Page-Total` | `int` | the total number of entries without pagination |

# Timestamp

Timestamps are always in UTC

# Time Range

For historical stats and/or logs where time range is needed, you can specify the time range in a few different ways:

| Query | Description |
| --- | --- |
| `?start=1430000000&end=1430864000` | specify the start / end |
| `?end=1430864000&duration=1d` | specify end time and duration |
| `?duration=1d` | specify duration, end will be now() in seconds |

# Aggregation

Aggregation works by giving a time range plus `interval` (e.g. `1d`, `1h`, `10m`) where aggregation function would be applied to.

Implementation-wise, aggregation happens at real time against fixed _windows_ or _bins_. E.g. for hourly aggregation, it will fall on 10:00-11:00 and not on 10:10-11:10.

That is, the query will be dynamically adjusted to align to the data available in our backend, with the actual start/end returned in the response. E.g. `?duration=1d&interval=1h` will give you latest 24 data points (end is implicitly now()). All time are in UTC.
