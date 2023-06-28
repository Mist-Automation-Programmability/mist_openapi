## Authentication

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

# Privileges

## Self

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
    "via_sso": false,
    "privileges": [
        {
            "scope": "org",
            "org_id": "9ff00eec-24f0-44d7-bda4-6238c81376ee",
            "name": "TestCompany",
            "role": "write",
            "views": ["location"],
            "msp_id": "9520c63a-f7b3-670c-0944-727774d5a722",
            "msp_name": "MSP",
            "msp_url": "https://...",
            "msp_logo_url": "https://.../logo/9520c63a-f7b3-670c-0944-727774d5a722.jpeg",
            "orggroup_ids": ["9ff00eec-24f0-44d7-bda4-6238c81376ee"],
        },
        {
            "scope": "site",
            "site_id": "d96e3952-53e8-4266-959a-45acd55f5114",
            "name": "Mist Office",
            "role": "admin",
            "org_id": "9ff00eec-24f0-44d7-bda4-6238c81376ee",
            "org_name": "TestCompany",
            "sitegroup_ids": ["581328b6-e382-f54e-c9dc-999983183a34"],
            "msp_id": "9520c63a-f7b3-670c-0944-727774d5a722",
            "msp_url": "https://...",
            "msp_logo_url": "https://.../logo/9520c63a-f7b3-670c-0944-727774d5a722.jpeg",
        },
        {
            "scope": "msp",
            "msp_id": "9520c63a-f7b3-670c-0944-727774d5a722",
            "name": "MSP",
            "msp_url": "https://...",
            "msp_logo_url": "https://.../logo/9520c63a-f7b3-670c-0944-727774d5a722.jpeg",
            "role": "admin"
        }
    ],
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
| `via_sso` | `boolean` | if admin login is via sso (via_sso is more restricted, password and email cannot be changed) |
| `privileges` | `list` | list of permission-against-scope |
| `scope` | `string` | org / site / msp |
| `org_id` | `string` | id of the org |
| `org_name` | `string` | name of the org (for a site belonging to org) |
| `msp_id` | `string` | id of the MSP (if the org belongs to an MSP) |
| `msp_name` | `string` | name of the MSP (if the org belongs to an MSP) |
| `msp_url` | `string` | custom url of the MSP (if the MSP belongs to an Advanced tier) |
| `msp_logo_url` | `string` | logo of the MSP (if the MSP belongs to an Advanced tier) |
| `orggroup_ids` | `list` | list of orggroup ids (if the org belongs to an MSP) |
| `name` | `string` | name of the org/site/MSP depending on object scope |
| `role` | `string` | access permissions: admin / write / read / helpdesk / installer |
| `views` | `list` | list of UI views, see [supported UI views](https://api.mist.com/api/v1/docs/Org#Custom-Roles) |
| `site_id` | `string` | id of the site |
| `sitegroup_ids` | `list` | list of sitegroup ids |
| `tags` | `list` | list of strings indicating capabilities. e.g. what to show/hide/disable/enable for this user |

### Response if two-factor authentication is pending

```json
Status: 200 OK

{
    "email": "test@mistsys.com",
    "privileges": null,
    "two_factor_required": true,
    "two_factor_passed": false
}

```

## Login with 2FA

When 2FA is enabled, there are two ways to login. 1. login with two_factor token (with Google Authenticator, etc) 2. login with email/password, SMS the token, and use /login/two_factor with the token

```
POST /api/v1/login

```

### Example

```json
{
    "email": "test@mistsys.com",
    "password": "foryoureyesonly",
    "two_factor": "123456"
}

```

### Parameter

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | **Required.** |
| `password` | `string` | **Required.** |
| `two_factor` | `string` | if two-factor authentication is enabled, this can be used to skip a separate call to /login/two_factor |

### Response if login successfully (i.e. email/password/two_factor matches)

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

```

### Response if login failed

```
Status: 400 Bad Request

```

### Response if email/password matches but `two_factor` doesn’t match

The session is partially created, /self reflects the pending two_factor authentication. Use /login/two_factor to login fully

```
Status: 401 Unauthorized
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

```

### Response if email/password matches but `two_factor` is not provided

The session is partially created, /self reflects the pending two_factor authentication. Use /login/two_factor to login fully

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

```

## Perform Two-Factor Authentication

```
POST /api/v1/login/two_factor

```

### Request

```json
{
    "two_factor": "123456"
}

```

### Response if provided two_factor code is correct

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

```

### Response if provided two_factor code is incorrect

```
Status: 401 Unauthorized

```

### Response if the user hasn’t login yet

```
Status: 401 Unauthorized

```

### Response if the user doesn’t have 2FA enabled

```
Status 404 Not Found

```

## Login with OAuth2

### Overview

A Mist account can be _linked_ to OAuth2 providers:

1. First, login with your Mist account
2. [Obtain the Authorization URL for Linking](https://api.mist.com/api/v1/docs/Auth#obtain-the-authorization-url)
3. Obtain the authorizaiton code by clicking / going through Authorization URL
4. Link Mist Account against OAuth2 Provider by using the authorization code
    

## Obtain Authorization URL for Linking

```
GET /api/v1/self/oauth/:provider
GET /api/v1/self/oauth/:provider?forward=http://manage.mist.com/oauth/callback.html

```

### Response

```json
{
    "linked": false,
    "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?....."
}

```

## Obtain Authorization Code

As OAuth2 flow goes through provider’s UI and back with the authorization code, there are two ways to get it 1. in JSON response, more usable for developers. Simply don’t specify the `forward` parameter when obtaining the authorization URL 2. as GET parameter, for UI where the user flow can be continued. Specify the landing page/url of your choice

### Response as JSON payload

```json
{
    "code": "4/S9tegDeLkrYg0L9pWNXV4cgMVbbr3SR9t693A2kSHzw"
}

```

### Response if forward is provided

```
HTTP/1.1 302 Found
Location: https://forwarded.host/path?code=:code

```

## Link Mist account with an OAuth2 Provider

```
POST /api/v1/self/oauth/:provider

```

### Request

```json
{
    "code": "4/S9tegDeLkrYg0L9pWNXV4cgMVbbr3SR9t693A2kSHzw"
}

```

### Response if OK

```json
Status: 200 OK

{
    "action": "oauth account linked",
    "id": "google-user-id"
}

```

### Response if Authorization Error

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

### Response

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

### Request

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

### Response

```json
{
    // ... whatever is in /api/v1/self

    "oauth_google": true
}

```

## Basic Auth

While our current UI uses Session / Cookie-based authentication, it’s also possible to do Basic Auth.

# API Token

Like many other API providers, it’s also possible to generate API Tokens to be used (in HTTP Header) for authentication. An API token ties to a Admin with equal or less privileges.

Notes:

1. an API token generated for a specific admin has the same privilege as the user
2. an API token will be automatically removed if not used for > 90 days
    

SSO admins cannot generate these API tokens. Refer Org level API tokens (/api/v1/docs/Org#api-token) which can have privileges of a specific Org/Site for more information.

## Create API Token

Note that the key is only available during creation time.

```
POST /api/v1/self/apitokens

```

### Response

```json
{
    "id": "7cc917df-630a-1508-1889-e18028052dde",
    "key": "MEaT4pEYG9hgHSUzddRUlT0TDRp3quf"
}

```

## Use API Token

To use API token, add a Authorization header when making an API request like the following:

```
Authorization: Token 

GET /api/v1/self

```

## List Current API Tokens

```
GET /api/v1/self/apitokens

```

### Response

```json
[
    {
        "id": "7cc917df-630a-1508-1889-e18028052dde",
        "key": "MEaT...3quf"
    }
]

```

## Delete an API Token

```
DELETE /api/v1/self/apitokens/:apitoken_id

```

## Change Admin information, password, and enable/disable two-factor auth

```
PUT /api/v1/self

```

### Request

```json
{
    "password": "foryoureyesonly",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "14081112222",
    "phone2": "14083334444",
    "persona": "security",
    "enable_two_factor": true
}

```

### Meanings

| Name | Type | Description |
| --- | --- | --- |
| `password` | `string` | new password |
| `first_name` | `string` | first name of logged-in user |
| `last_name` | `string` | last name of logged-in user |
| `phone` | `string` | phone number (numbers only, including country code) |
| `phone2` | `string` | secondary phone number |
| `enable_two_factor` | `boolean` | to enable or disable two-factor authentication |
| `two_factor_verified` | `boolean` | if enable_two_factor=true, whether it’s verified. |

- `enable_two_factor`. Note that when two-factor authentication is enabled (from disabled-state), the `two_factor_seed` is re-generated and `two_factor_verified` is reset to false. The OTP will need to be verified before it takes effect.
    

## Change Email

We require the user to verify that they actually own the email address they intend to change it to.

```
POST /api/v1/self/update

```

### Request

```json
{
    "email": "new@mistsys.com"
}

```

### Meanings

| Name | Type | Description |
| --- | --- | --- |
| `email` | `string` | new email address |

### Response if OK

```
Status: 200 OK

```

After the API call, the user will receive an email to the new email address with a link like https://manage.mist.com/verify/update?expire=:exp_time&email=:admin_email&token=:token

Upon clicking the link, the user is provided with a login page to authenticate using existing credentials. After successful login, the email address of the user gets updated

Note: The request parameter `email` can be used by UI to validate that the current session (if any) belongs to the admin or provide a login page (by pre-populating the email on login screen). UI can also use the request parameter `expire` to validate token expiry.

### Response if invalid email address

```
Status: 400 Bad Request

```

### Response if new email address already exists

```json
Status: 400 Bad Request

{
    "detail": "email already existed"
}

```

## Verify Email change

```
POST /api/v1/self/update/verify/:token

```

### Response if OK

With correct verification, the email address of the user will be updated

```
Status: 200 OK

```

### Response if invalid or expired token

```json
Status: 400 Bad Request

{
    "detail": "invalid token"
}

```

### Response if request comes from authenticated users other than admin

```json
Status: 400 Bad Request

{
    "detail": "invalid token"
}

```

### Response if new email address already exists

```json
Status: 400 Bad Request

{
    "detail": "email already existed"
}

```

## Generate QR code for verification

```
GET /api/v1/self/two_factor/token?by=qrcode

```

### Request Parameters

| Name | Type | Description |
| --- | --- | --- |
| `by` | `string` | qrcode |

## Verify Two-factor (OTP)

To verify two-factor authentication by using a code generated by app (e.g. Google Authenticator, Authy) or by SMS. Upon successful verification, the `otp_verified` will be set to true if it hasn’t already been.

```
POST /api/v1/self/two_factor/verify

```

### Request

```json
{
    "two_factor": "123456"
}

```

### Response when 2FA verification is successful

```
Status: 200 OK

```

# Register

## Register a new admin and his/her org

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

### reCAPTCHA

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

## Verify registration

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

## Recover Password

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

## Verify Recover Password

```
POST /api/v1/recover/verify/:token

```

### Response

With correct verification, the user will be authenticated. UI can then prompt for new password

```
Status: 200 OK
Set-Cookie: csrftoken=vwvBuq9qkqaKh7lu8tNc0gkvBfEaLAmx; expires=Tue, 15-Mar-2016 19:47:20 GMT; Max-Age=31449600; Path=/

```

# Leave

To delete ones account and every associated with it. The effects:

1. the account would be deleted
2. any orphaned Org (that only has this account as admin) will be deleted
3. along with all data with Org (sites, wlans, devices) will be gone.
    

## Delete Account

```
DELETE /api/v1/self

```

### Response

```
Status: 200 OK

```

### Response if any of the org to be deleted still has inventory

```json
Status: 400 Bad Request

{ 
    "detail": "inventory not empty",
    "org_id": "2818e386-8dec-2562-9ede-5b8a0fbbdc71"
}

```

# Audit Logs

Audit logs records all administrative activities done by current admin across all orgs

## Get a list of change logs across all Orgs for current admin

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

see [Pagination](https://api.mist.com/api/v1/docs/Overview#pagination)

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

# Integration

## Get Zendesk Access URL

Basically, 1. user tries to access https://mist.zendesk.com/videos/quickstart.html 2. zendesk detects that the user is not authenticated, redirect the user to a URL we specified with return_to= 3. after we authenticate the user, redirect the user back to https://mist.zendesk.com/access/jwt?jwt=&return_to=

for 3, the URL can be generated by calling this API

```
GET /api/v1/self/sso/zendesk?return_to=

```

### Request Parameters

| Name | Type | Description |
| --- | --- | --- |
| `return_to` | `string` | the URL the user intended to go |

### Response 

```json
{
    "url": "https://mist.zendesk.com/access/jwt?jwt=eyJhbGciO...&return="
}

```

## Get UserVoice Access URL

Uservoice works similar to Zendesk. UI needs to 1. handle `/uservoice/sso_login?return_to=%s`, allow the user to login, then call this API and forward the user to it 2. for a login user, call this API to get a link to launch UserVoice

```
GET /api/v1/self/sso/uservoice?return_to=

```

### Request Parameters

| Name | Type | Description |
| --- | --- | --- |
| `return_to` | `string` | the URL the user intended to go |

### Response 

```json
{
    "url": "http://ideas.mist.com/forums/912934-feature-requests?sso=eyJhbGciO..."
}

```

## Get TalentLMS Access URL

TalentLMS works similar to Zendesk. UI needs to 1. handle `/talentlms/sso_login?return_to=%s`, allow the user to login, then call this API and forward the user to it 2. for a login user, call this API to get a link to launch TalentLMS

```
GET /api/v1/self/sso/talentlms?return_to=

```

### Request Parameters

| Name | Type | Description |
| --- | --- | --- |
| `return_to` | `string` | the URL the user intended to go |

### Response

```json
{
    "url": "https://mist.talentlms.com/index/autologin/key:atwnztuy4ui2nmcs1531039"
}

```

# Misc

## Get Registration Information

```
GET /api/v1/register/recaptcha

```

### Response

```json
{
    "flavor": "google",
    "required": true,
    "sitekey": "6LdAewsTAAAAAE25XKQhPEQ2FiMTft-WrZXQ5NUd"
}

```

## Claim CMX Orgs

For CMX customers, this API allow them to access the CMX Tenant via their Mist account.

```
POST /api/v1/self/claim_cmx

```

### Request

```json
{
    "username": "cmxuser1@abc.com",
    "password": "password"
}

```

### Request Parameters

| Name | Type | Description |
| --- | --- | --- |
| `username` | `string` | CMX username |
| `password` | `string` | CMX password |