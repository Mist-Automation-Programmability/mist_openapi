The current rate limiting is 5000 API calls per hour and is reset at the hourly boundary. If you need more, please contact our support about your use case. It is possible that there are other APIs that can better serve you or new APIs we could have created to do what you’re trying to do.

NOTE: `/api/v1/login` is rate-limited much sooner (after 3 login failures) to prevent brute-force attack

#### Response when the request is rate-limited

```
Status: 429 Too Many Requests
Retry-After: 798


```
