# IP Addresses used by Mist to send the Webhooks
It is possible to filter incoming Webhooks based on the Source IP addresses. IP addresses are available at the end of this page: [Ports to enable on your firewall
](https://www.mist.com/documentation/ports-enable-firewall/)

# Securing Webhooks with `http-post` type

## The `secret` parameter
When using `http-post` webhooks type (unlike `splunk` type), the “secret” parameter in the webhook configuration is used by the Mist Cloud to sign the webhook message. This signature can be used to authenticated the Mist Cloud and validate the body has not been manipulated or corrupted. 

This signature is added in the following HTTP headers :
```
X-Mist-Signature-v2: HMAC_SHA256(secret, body)
X-Mist-Signature: HMAC_SHA1(secret, body)
```

It’s not required to parse the body to calculate the signature on the Webhook Collector side, the raw data is enough. Here is an example in Python:
```python
import hmac
import hashlib
import json
    
signature = req.headers['X-Mist-Signature-v2'] if "X-Mist-Signature-v2" in req.headers else None
key = str.encode(secret)
message = req.data
digester = hmac.new(key, message, hashlib.sha256).hexdigest()
if signature != digester:
    console.error("Webhook signature doesn't match")
    return '', 401
else:
    console.info("Webhook signature confirmed")
    content = req.get_json()
    try:
        # do something with the webhook body
        console.info("Webhook Body processed")
        return '', 200
    except:
        console.error("Error durring Webhook Body processing")
        return '', 500
```

## Custom Headers
It is possible to add a customer headers, which will be added in the HTTP headers sent by the Mist Cloud.

To do so, the custom headers must be added in the Webhook configuration under the `headers` property (as a dictionnaty)

```json
{
    "name": "audits",
    "type": "http-post",
    "url": "https://username:password@hooks.abc.com/uri/...",
    "secret": "secret",
    "headers":{
        "x-custom-1": "your_custom_header_value1",
        "x-custom-2": "your_custom_header_value2"
    },
    "verify_cert": false,
    "enabled": true,
    "topics": [ "audits" ]
}
```

More information here: https://api.mist.com/api/v1/docs/Site#webhooks

# Securing Webhooks with `splunk` type
The Mist Webhooks configured with the `splunk`type are supporting the configuration of the Splunk HEC (HTTP Event Collector) Token. 

This Token is generated by Splunk during the HEC configuration. More details about the HEC configuration and the Splunk HEC Token can be found in the [Splunk Documentation](https://docs.splunk.com/Documentation/Splunk/9.0.5/Data/UsetheHTTPEventCollector#Send_data_to_HTTP_Event_Collector), but:

>Tokens are entities that let logging agents and HTTP clients connect to the HEC input. Each token has a unique value, which is a 128-bit number that is represented as a 32-character globally unique identifier (GUID). Agents and clients use a token to authenticate their connections to HEC. When the clients connect, they present this token value. If HEC receives a valid token, it accepts the connection and the client can deliver its payload of application events in either text or JavaScript Object Notation (JSON) format.
>
>HEC receives the events and Splunk Enterprise indexes them based on the configuration of the token. HEC uses the source, source type, and index that was specified in the token. If a forwarding output group configuration exists on a Splunk Enterprise instance, HEC forwards the data to indexers in that output group.

The Webhook configuration in Mist will looks like:
```json
{
    "name": "splunk-mist-audits",
    "type": "splunk",
    "url": "https://my.splunk.host:8088/services/collector",
    "splunk_token": "7d34bcab-7d3d-49d8-adcf-67747e1f3704",
    "verify_cert": false,
    "enabled": true,
    "topics": [ "audits" ]
}
```

