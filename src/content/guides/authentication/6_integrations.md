# Get Zendesk Access URL

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

# Get UserVoice Access URL

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

# Get TalentLMS Access URL

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