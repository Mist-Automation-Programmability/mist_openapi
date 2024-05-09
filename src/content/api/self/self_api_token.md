Like many other API providers, it's also possible to generate API Tokens to be used (in HTTP Header)
 for authentication. An API token ties to a Admin with equal or less privileges.

**Notes:**

* an API token generated for a specific admin has the same privilege as the user
* an API token will be automatically removed if not used for > 90 days
* SSO admins cannot generate these API tokens. Refer [Org level API tokens](page:api/orgs/orgs_api_tokens) which can have privileges of a specific Org/Site for more information.