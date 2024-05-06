Authentication covers how to login (authenticate against the API endpoint) and get the privileges, against which organization(s) and site(s) the admin is granted to.

# See If Login Already

Get ‘whoami’ and privileges (which org and which sites I have access to)

```
GET /api/v1/self
```

#### Response if a valid session has been created

```json
Status: 200 OK

{
    "email": "test@mistsys.com",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "14081112222",
    "phone2": "",
    "via_sso": false,
    "tags": [ "has_8021x", "mist" ]
}
```

#### Definitions

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | email of logged-in user |
| `first_name` | `string` | first name of logged-in user |
| `last_name` | `string` | last name of logged-in user |
| `phone` | `string` | phone number (numbers only, including country code) |
| `phone2` | `string` | secondary phone number (numbers only, including country code) |
| `via_sso` | `boolean` | an admin alogin via_sso is more restircted. (password and email cannot be changed) |
| `tags` | `list` | list of strings indicating capabilities. e.g. what to show/hide/disable/enable for this user |

#### Response if two-factor authentication is pending

```json
Status: 200 OK

{
    "email": "test@mistsys.com",
    "privileges": null,
    "two_factor_required": true,
    "two_factor_passed": false
}
```


# Login Lookup

```
POST /api/v1/login/lookup
```

#### Example

```json
{
    "email": "test@mistsys.com"
}
```

#### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** |

#### Response if user does not exist

```json
Status: 404 Not Found
```

#### Response if local account exists

```json
Status: 200 OK

```

#### Response if SSO user exists

```json
Status: 200 OK

{
    "sso_url": "https://my.sso/idp_sso_url"
}
```

# Login

```
POST /api/v1/login
```

#### Example

```json
{
    "email": "test@mistsys.com",
    "password": "foryoureyesonly"
}
```

#### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** |
| `password` | `string` | **Required.** |

#### Response if login successfully (i.e. email/password matches)

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/
```

#### Response if login failed

```json
Status: 400 Bad Request

{
    "detail": "sso admin login needs to be initiated by IdP",
    "forward_url": "https://my.sso/idp_sso_url"
}
```

# Login with 2FA

When 2FA is enabled, there are two ways to login. 1. login with two_factor token (with Google Authenticator, etc) 2. login with email/password, SMS the token, and use /login/two_factor with the token

```
POST /api/v1/login
```

#### Example

```json
{
    "email": "test@mistsys.com",
    "password": "foryoureyesonly",
    "two_factor": "123456"
}
```

#### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** |
| `password` | `string` | **Required.** |
| `two_factor` | `string` | if two-factor authentication is enabled, this can be used to skip a separate call to /login/two_factor |

#### Response if login successfully (i.e. email/password/two_factor matches)

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/
```

#### Response if login failed

```
Status: 400 Bad Request
```

#### Response if email/password matches but `two_factor` doesn’t match

The session is partially created, /self reflects the pending two_factor authentication. Use /login/two_factor to login fully

```
Status: 401 Unauthorized
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/
```

#### Response if email/password matches but `two_factor` is not provided

The session is partially created, /self reflects the pending two_factor authentication. Use /login/two_factor to login fully

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/
```

# Perform Two-Factor Authentication

```
POST /api/v1/login/two_factor
```

#### Request

```json
{
    "two_factor": "123456"
}
```

#### Response if provided two_factor code is correct

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/
```

#### Response if provided two_factor code is incorrect

```
Status: 401 Unauthorized
```

#### Response if the user hasn’t login yet

```
Status: 401 Unauthorized
```

#### Response if the user doesn’t have 2FA enabled

```
Status 404 Not Found
```

# OAuth2

## Process Overview

A Mist account can be _linked_ to OAuth2 providers:

1. First, login with your Mist account
2. Obtain the Authorization URL for Linking
3. Obtain the authorizaiton code by clicking / going through Authorization URL
4. Link Mist Account against OAuth2 Provider by using the authorization code
    

## Obtain Authorization URL for Linking

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

## Obtain Authorization Code

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

### Link Mist account with an OAuth2 Provider

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

## Obtain Authorization URL for Login

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

## Login via OAuth2

```
POST /api/v1/login/oauth/:provider
```

#### Request

```json
{
    "code": "4/S9tegDeLkrYg0L9pWNXV4cgMVbbr3SR9t693A2kSHzw"
}
```

## Unlink OAuth2 Provider

```
DELETE /api/v1/self/oauth/:provider
```

## See Linked OAuth2 Provider

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
