
import os
import yaml

# schemas = {}
# with open("mist.openapi.components.yml", "r") as f:
#     data = yaml.load(f, Loader=yaml.loader.SafeLoader)
#     schemas = data.get("components", {}).get("parameters")

# for schema in schemas:
#     schema_data = schemas[schema]
#     with open(f"./components/parameters/{schema}.yml", "w") as f:
#         yaml.dump(schema_data, f)


folders = ["schemas", "responses", "parameters"]


for folder in folders:
    files = os.listdir(f"./components/{folder}/")
    data = {}
    out_file = f"./mist.openapi.{folder}.yml"
    for file in files:
        if file != "_index.yml":
            filename = ".".join(file.split(".")[:-1])
            with open(f"./components/{folder}/{file}") as f_in:
                data[filename] = yaml.safe_load(f_in)
    with open(out_file, "w") as f_out:
        yaml.dump(data, f_out)


