import os

folders = ["./components/schemas", "./components/responses", "./components/parameters"]

for folder in folders:
    files = os.listdir(folder)
    if "_index.yml" in files:
        i = files.index("_index.yml")
        files.pop(i)
    with open(f"{folder}/_index.yml", 'w') as f:
        for file in files:
            filename = ".".join(file.split(".")[:-1])
            f.write(f"{filename}:\r\n")
            f.write(f"  $ref: \"./{file}\"\r\n")