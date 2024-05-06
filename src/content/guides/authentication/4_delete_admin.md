To delete ones account and every associated with it. The effects:

1. the account would be deleted
2. any orphaned Org (that only has this account as admin) will be deleted
3. along with all data with Org (sites, wlans, devices) will be gone.


# Delete Account

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
