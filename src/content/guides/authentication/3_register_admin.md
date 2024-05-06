# Register a new admin and his/her org

```
POST /api/v1/register

```

### Request

```json
{
    "email": "test@mistsys.com",
    "password": "foryoureyesonly",
    "first_name": "John",
    "last_name": "Smith",
    "org_name": "TestCompany",
    "recaptcha": "see https://www.google.com/recaptcha/",
    "referer_invite_token": "Dm2gtT8dwMeM4Bc2E8FLIaA96VHOjPat",
    "return_to": "http://mist.zendesk.com/hc/quickstart.pdf",
    "account_only": false,
    "allow_mist": false,
    "invite_code": "MISTROCKS"
}

```

### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** max length is 64 |
| `password` | `string` | **Required.** |
| `first_name` | `string` | **Required.** |
| `last_name` | `string` | **Required.** |
| `org_name` | `string` | **Required.** |
| `recaptcha` | `string` | reCAPTCHA |
| `referer_invite_token` | `string` | optional, the invite token to apply after account creation |
| `return_to` | `string` | optional, the url the user should be redirected back to |
| `account_only` | `boolean` | skip creating initial setup if true, default is false |
| `allow_mist` | `boolean` | whether to allow Mist to look at this org, default is False |
| `invite_code` | `string` | required initially |

## reCAPTCHA

Google reCAPTCHA is the choice to prevent bot registration

```
It needs this script

and this 
```

### Response if registration is successful

```
Status: 200 OK

```

An email will also be sent to the user with a link to https://manage.mist.com/verify/register?token=:token

# Verify registration

```
POST /api/v1/register/verify/:token

```

### Response if successful

With correct verification, the admin account will be created and the authenticated

```json
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

{
    // optionally, the URL stored in the registration flow is remembered
    "return_to": "http://mist.zendesk.com/hc/quickstart.pdf"
}

```

### Response if successful but failed to apply the invitation automatically

With correct verification, the admin account will be created and the authenticated

```json
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

{
    "invite_not_applied": true,

    // same information
    "detail":"password policy not met",
    "min_length": 8
}

```

### Response if secret is invalid

```json
Status: 404 Not Found

{
    "detail": "Not found."
}

```

### Response if verification expired

```json
Status: 400 Bad Request

{
    "detail": "expired"
}

```

### Response if already registered

```json
Status: 400 Bad Request

{
    "detail": "already registered"
}

```

# Recover Password

```
POST /api/v1/recover

```

### Request

```json
{
    "email": "test@mistsys.com",
    "recaptcha": "see https://www.google.com/recaptcha/"
}

```

### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** max length is 64 |
| `recaptcha` | `string` | reCAPTCHA |

### Response

```
Status: 200 OK

```

An email will also be sent to the user with a link to https://manage.mist.com/verify/recover?token=:token

# Verify Recover Password

```
POST /api/v1/recover/verify/:token

```

### Response

With correct verification, the user will be authenticated. UI can then prompt for new password

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

```
