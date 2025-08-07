import yaml
import re
import os
SPEC_FILE_IN="./openapi.yaml"
OUT_FOLDER="../src/spec/components"
PARTS=["parameters", "responses", "schemas"]
with open(SPEC_FILE_IN, "r") as f:
    DATA = yaml.load(f, Loader=yaml.loader.SafeLoader)
    COMP = DATA["components"]


REG = r"#\/components\/(?P<t>[^\/]*)\/(?P<n>[^\']*)"
if not os.path.isdir(f"{OUT_FOLDER}"):
    os.makedirs(f"{OUT_FOLDER}")

for part in PARTS:
    print(part)
    for file_name, file_data in COMP.get(part).items():
        if not os.path.isdir(f"{OUT_FOLDER}/{part}"):
            os.makedirs(f"{OUT_FOLDER}/{part}")
        file_path=f"{OUT_FOLDER}/{part}/{file_name}.yaml"
        if not file_data.get("title"):
            file_data["title"] = (file_name.replace("_ ", " ")).title()
        file_data_string = yaml.dump(file_data)
        refs = re.findall(REG, file_data_string)
        file_data_string = re.sub(REG, "../\\1/\\2.yaml", file_data_string)
        with open(file_path, "w") as f_out:
            f_out.write(file_data_string)
