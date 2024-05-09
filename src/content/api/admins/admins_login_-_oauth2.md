A Mist account can be linked to OAuth2 providers:
1. First, login with your Mist account
2. Obtain the Authorization URL for Linking with [Get Oauth 2 Authorization Url for Login]($e/Admins%20Login%20-%20OAuth2/getOauth2AuthorizationUrlForLogin).
As OAuth2 flow goes through provider's UI and back with the authorization code, there are two ways to get it:
  * in JSON response, more usable for developers. Simply don\'t specify the `forward` parameter when obtaining the authorization URL
  * as GET parameter, for UI where the user flow can be continued. Specify the landing page/url of your choice 
3. Obtain the authorizaiton code by clicking / going through Authorization URL Link Mist Account against OAuth2 Provider by using the authorization code