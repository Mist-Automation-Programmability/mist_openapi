A Mist account can be _linked_ to OAuth2 providers:

1. First, login with your Mist account
2. Obtain the Authorization URL for Linking
3. Obtain the authorizaiton code by clicking / going through Authorization URL
4. Link Mist Account against OAuth2 Provider by using the authorization code
    

# Obtain Authorization URL for Linking

```
GET /api/v1/self/oauth/:provider
GET /api/v1/self/oauth/:provider?forward=http://manage.mist.com/oauth/callback.html
```

#### Response

```json
{
    "linked": false,
    "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?....."
}
```

# Obtain Authorization Code

As OAuth2 flow goes through provider’s UI and back with the authorization code, there are two ways to get it 1. in JSON response, more usable for developers. Simply don’t specify the `forward` parameter when obtaining the authorization URL 2. as GET parameter, for UI where the user flow can be continued. Specify the landing page/url of your choice

#### Response as JSON payload

```json
{
    "code": "4/S9tegDeLkrYg0L9pWNXV4cgMVbbr3SR9t693A2kSHzw"
}
```

#### Response if forward is provided

```
HTTP/1.1 302 Found
Location: https://forwarded.host/path?code=:code
```

# Link Mist account with an OAuth2 Provider

```
POST /api/v1/self/oauth/:provider
```

#### Request

```json
{
    "code": "4/S9tegDeLkrYg0L9pWNXV4cgMVbbr3SR9t693A2kSHzw"
}
```

#### Response if OK

```json
Status: 200 OK

{
    "action": "oauth account linked",
    "id": "google-user-id"
}
```

#### Response if Authorization Error

```json
Status: 400 Bad Request

{
    "error": "access_denied",
    "error_description": "The resource owner or authorization server denied the request."
}
```

# Obtain Authorization URL for Login

```
GET /api/v1/login/oauth/:provider
GET /api/v1/login/oauth/:provider?forward=http://manage.mist.com/oauth/callback.html
```

#### Response

```json
{
    "client_id": "173131512-mpbnju32.apps.googleusercontent.com",
    "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?....."
}
```

# Login via OAuth2

```
POST /api/v1/login/oauth/:provider
```

#### Request

```json
{
    "code": "4/S9tegDeLkrYg0L9pWNXV4cgMVbbr3SR9t693A2kSHzw"
}
```

# Unlink OAuth2 Provider

```
DELETE /api/v1/self/oauth/:provider
```

# See Linked OAuth2 Provider

```
GET /api/v1/self
```

#### Response

```json
{
    // ... whatever is in /api/v1/self

    "oauth_google": true
}
```

# Basic Auth

While our current UI uses Session / Cookie-based authentication, it’s also possible to do Basic Auth.

# Logout

```
POST /api/v1/logout
```

#### Response

```json
Status: 200 OK

{
    // if configured in SSO as custom_logout_url
    "forward_url": "https://my.sso/custom_logout_url"
}
```
