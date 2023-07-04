# Authentication

Authentication covers how to login (authenticate against the API endpoint) and get the privileges, against which organization(s) and site(s) the admin is granted to.

# Login

## See If Login Already

Get ‘whoami’ and privileges (which org and which sites I have access to)

```
GET /api/v1/self

```

### Response if a valid session has been created

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

### Definitions

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | email of logged-in user |
| `first_name` | `string` | first name of logged-in user |
| `last_name` | `string` | last name of logged-in user |
| `phone` | `string` | phone number (numbers only, including country code) |
| `phone2` | `string` | secondary phone number (numbers only, including country code) |
| `via_sso` | `boolean` | an admin alogin via_sso is more restircted. (password and email cannot be changed) |
| `tags` | `list` | list of strings indicating capabilities. e.g. what to show/hide/disable/enable for this user |

## Login Lookup

```
POST /api/v1/login/lookup

```

### Example

```json
{
    "email": "test@mistsys.com"
}

```

### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** |

### Response if user does not exist

```json
Status: 404 Not Found

```

### Response if local account exists

```json
Status: 200 OK


```

### Response if SSO user exists

```json
Status: 200 OK

{
    "sso_url": "https://my.sso/idp_sso_url"
}

```

## Login

```
POST /api/v1/login

```

### Example

```json
{
    "email": "test@mistsys.com",
    "password": "foryoureyesonly"
}

```

### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** |
| `password` | `string` | **Required.** |

### Response if login successfully (i.e. email/password matches)

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

```

### Response if login failed

```json
Status: 400 Bad Request

{
    "detail": "sso admin login needs to be initiated by IdP",
    "forward_url": "https://my.sso/idp_sso_url"
}

```

## Logout

```
POST /api/v1/logout

```

### Response

```json
Status: 200 OK

{
    // if configured in SSO as custom_logout_url
    "forward_url": "https://my.sso/custom_logout_url"
}

```
