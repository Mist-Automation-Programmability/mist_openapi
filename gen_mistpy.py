import os
import yaml

openapi_file = "./Mist.openapi_bundled.yml"

def create_folder(path, folder_name):
    full_path = os.path.join(path, folder_name)
    if not os.path.isdir(full_path):
        os.mkdir(full_path)

def save_file(path, file_name, data):
    full_path = os.path.join(path, file_name)
    with open(file_name, "w") as f:
        f.write(data)


def load_openapi(file_path):
    with open(file_path, 'r') as f:
        


if __name__ == "__main__":
    