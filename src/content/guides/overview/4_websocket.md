# Sample UI codes

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

# Sample Python Code

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