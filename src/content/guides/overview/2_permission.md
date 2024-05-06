Mist API follow REST principles where GET requires `read` role, POST / PUT / DELETE requires `write` role.

# CSRF

All POST / PUT / DELETE APIs needs to have CSRF token in the AJAX Request header. This protects the website against [Cross Site Request Forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery).

```
X-CSRFToken: vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx

```

This token can be retrieved from the `cookies[csrftoken]`, which is sent during Login
