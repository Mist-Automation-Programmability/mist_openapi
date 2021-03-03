# Juniper-Mist OpenAPI Standard 3.0 library

Juniper Mist APIs in Open API Standard 3.0 format.

Live documentation: https://doc.mist-lab.fr/

## Files
#### Mist.openapi_collection.yml:
This file includes all the API endpoints, and is using the OAS models in the `models`folder. It is using YAML format.
#### Mist.openapi_bundled.yml:
This is a "standalone" version of the Mist.openapi_collection version. It includes all the API endpoints and all the models. It is using YAML format.
#### Mist.openapi_bindled.json:
This is a "standalone" version of the Mist.openapi_collection version. It includes all the API endpoints and all the models. It is using JSON format.


## Notes
This library may be used to automate the client SDK generation. It is currently tested with [openapi-generator](https://github.com/OpenAPITools/openapi-generator) and Python, but it may work with others code generators and other languages.

Generated code is available [here](https://github.com/tmunzer/Mist-OAS3.0-SDK)
