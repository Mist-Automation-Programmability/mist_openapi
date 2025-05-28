import os

folders = ["./components/schemas", "./components/responses", "./components/parameters"]

for folder in folders:
    files = os.listdir(folder)
    if "_index.yaml" in files:
        i = files.index("_index.yaml")
        files.pop(i)
    with open(f"{folder}/_index.yaml", 'w') as f:
        for file in files:
            filename = ".".join(file.split(".")[:-1])
            f.write(f"{filename}:\r\n")
            f.write(f"  $ref: \"./{file}\"\r\n")