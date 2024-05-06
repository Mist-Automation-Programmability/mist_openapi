# Get Registration Information

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

# Claim CMX Orgs

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