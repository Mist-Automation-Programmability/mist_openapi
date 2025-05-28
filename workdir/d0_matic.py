"""
This script is generating the spec files from the main openapi spec (single file) based on the documentation tag
Can be filtered to one or multiple spec files based on the .filters file
"""
import yaml
import re
import json
import sys
import os
import shutil

SPEC_FILE_IN="./mist.openapi.yaml"
SPEC_FOLDER_OUT="../src/spec"
FILTER_FILE="./.filters"

with open(FILTER_FILE, 'r') as filter_file:
    filters_string = filter_file.read().split("=")[1].split("#")[0]
    FILTER = filters_string.split(",")

with open(SPEC_FILE_IN, "r") as f:
    DATA = yaml.load(f, Loader=yaml.loader.SafeLoader)

ORDER = [
    "openapi",
    "info",
    "servers",
    "security",
    "tags",
    "paths",
    "components",
]

def clean_out_folder():
    full_path = os.path.join(os.path.curdir, SPEC_FOLDER_OUT)
    shutil.rmtree(full_path)
    os.mkdir(full_path)


def check_folder(folder_path):
    full_path = os.path.join(os.path.curdir, SPEC_FOLDER_OUT, folder_path)
    if not os.path.isdir(full_path):
        os.mkdir(full_path)







#####################################################
clean_out_folder()
os.mkdir(f"{SPEC_FOLDER_OUT}/api")
file = f"{SPEC_FOLDER_OUT}/api/mist.openapi.yaml"
with open(file, "w")  as oas_out_file:
    for item in ORDER:
        yaml.dump({item: DATA[item]}, oas_out_file)