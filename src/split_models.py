

import yaml

schemas = {}
with open("mist.openapi.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.loader.SafeLoader)
    schemas = data.get("components", {}).get("schemas")

for i in schemas:
    print(i)