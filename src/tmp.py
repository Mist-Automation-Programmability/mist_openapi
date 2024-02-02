

import yaml

schemas = {}
with open("mist.openapi.components.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    schemas = data.get("components", {}).get("parameters")

for schema in schemas:
    schema_data = schemas[schema]
    with open(f"./components/parameters/{schema}.yml", "w") as f:
        yaml.dump(schema_data, f)
